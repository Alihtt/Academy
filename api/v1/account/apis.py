from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import LoginSerializer, LoginVerifySerializer, UserInfoSerializer
from django.core.cache import cache
from random import randint
from django.conf import settings
from account.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from api.tasks import send_otp_task
from django.core.exceptions import ObjectDoesNotExist
from api.prefix import LOGIN_OTP_PREFIX


class Login(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.POST)
        if ser_data.is_valid():
            phone_number = ser_data.data['phone_number']
            cache_key = f'{LOGIN_OTP_PREFIX}:{phone_number}'
            if not cache.get(cache_key):
                otp_code = randint(100000, 999999)
                cache.set(cache_key, otp_code, timeout=settings.CACHE_TTL)
                send_otp_task.delay(phone_number, otp_code)
                return Response({'message': f'کد ورود ارسال شد'},
                                status=status.HTTP_200_OK)
            return Response({'message': f'کد ورود قبلی همچنان معتبر است'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginVerify(GenericAPIView):
    serializer_class = LoginVerifySerializer
    user_serializer_class = UserInfoSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.POST)
        if ser_data.is_valid():
            phone_number = ser_data.data['phone_number']
            cache_key = f'{LOGIN_OTP_PREFIX}:{phone_number}'
            otp_code = cache.get(cache_key)
            if otp_code == ser_data.data['code']:
                try:
                    user = User.objects.get(phone_number=phone_number)
                except ObjectDoesNotExist:
                    user = User.objects.create_user(phone_number=phone_number)
                refresh = RefreshToken.for_user(user)
                user_ser_data = self.user_serializer_class(instance=user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': user_ser_data.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'کد ورود صحیح نمیباشد'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
