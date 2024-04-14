from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSendCodeSerializer, UserRegisterSendCodeDoneSerializer
from django.core.cache import cache
from random import randint
from django.conf import settings
from account.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from api.tasks import send_otp_task


class RegisterUserSendCode(GenericAPIView):
    serializer_class = UserRegisterSendCodeSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.POST)
        if ser_data.is_valid():
            random_code = randint(10000, 99999)
            cache.set(ser_data.data['phone_number'], random_code, timeout=settings.CACHE_TTL)
            send_otp_task.delay(ser_data.data['phone_number'], random_code)
            return Response({'success': f'expire time: {settings.CACHE_TTL}s'},
                            status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserSendCodeDone(GenericAPIView):
    serializer_class = UserRegisterSendCodeDoneSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.POST)
        if ser_data.is_valid():
            phone_number = ser_data.data['phone_number']
            random_code = cache.get(phone_number)
            if random_code == ser_data.data['code']:
                user = User.objects.create_user(phone_number=phone_number)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'code does not match'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
