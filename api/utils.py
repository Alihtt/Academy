from rest_framework.serializers import ValidationError
from django.conf import settings
import requests
import re


def validate_phone_number(data: str):
    if not re.match(settings.PHONE_NUMBER_REGEX, data):
        raise ValidationError('شماره تلفن همراه معتبر نمیباشد')
    return data


def send_otp_code(phone_number, code):
    try:
        api = settings.SMS_API.format(receiver_number=phone_number, note=settings.SMS_TEXT.format(code=code))
        response = requests.get(api)
        response_text = response.text
        if not response_text or 'error' in response_text:
            return False
        return response_text

    except Exception as e:
        print(e)
