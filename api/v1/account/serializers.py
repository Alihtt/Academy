from rest_framework import serializers
from account.models import User
import unidecode
import re


class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ("phone_number", "email", 'first_name', 'last_name', "password", "password_confirm")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        del validated_data["password_confirm"]
        return User.objects.create_user(**validated_data)

    def validate_phone_number(self, data):
        phone_number_regex = r"^(09(0[1-5]|1[0-9]|2[0-9]|3[0-9]|4[12]|9[0-4]|34|91|00|90|92|93|94|95|96|97|98|99))[0-9]{7}$"
        phone_number = unidecode.unidecode(data)
        if re.match(phone_number_regex, phone_number):
            return phone_number
        else:
            raise serializers.ValidationError('phone number is not valid')

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Passwords must match")
        else:
            return data


class UserForgotPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Passwords must match")
        else:
            return data
