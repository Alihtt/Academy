from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ViewSet
from .serializers import UserRegisterSerializer, UserForgotPasswordSerializer
from rest_framework.permissions import IsAuthenticated


class UserViewSet(ViewSet):
    serializer_class = UserRegisterSerializer

    def list(self, request):
        ser_data = self.serializer_class(request.user)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def create(self, request):
        ser_data = self.serializer_class(data=request.POST)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class ForgotPasswordView(GenericAPIView):
    serializer_class = UserForgotPasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser_data = self.serializer_class(data=request.POST)
        if ser_data.is_valid():
            request.user.set_password(ser_data.validated_data['password'])
            request.user.save()
            return Response({'success': 'You password successfully changed'}, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)