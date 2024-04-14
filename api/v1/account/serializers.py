from rest_framework import serializers
from account.models import User
from api.utils import validate_phone_number


class BaseUserRegisterSendCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, validators=[validate_phone_number])

    class Meta:
        abstract = True

    def validate(self, data):
        user = User.objects.filter(phone_number=data["phone_number"]).exists()
        if user:
            raise serializers.ValidationError('کاربر با این شماره تلفن ثبت نام شده است')
        return data


class UserRegisterSendCodeSerializer(BaseUserRegisterSendCodeSerializer):
    pass


class UserRegisterSendCodeDoneSerializer(BaseUserRegisterSendCodeSerializer):
    code = serializers.IntegerField(required=True)

    def validate_code(self, data):
        if len(str(data)) != 6:
            raise serializers.ValidationError('کد شما باید 6 رقمی باشد')
        return data


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'status', 'is_admin')
