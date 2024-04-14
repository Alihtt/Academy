from rest_framework.serializers import ValidationError
import requests
import re

PHONE_NUMBER_REGEX = r"^(09(0[1-5]|1[0-9]|2[0-9]|3[0-9]|4[12]|9[0-4]|34|91|00|90|92|93|94|95|96|97|98|99))[0-9]{7}$"
SMS_API = 'https://sms.segalnet.net/send_via_get/send_sms.php?username=bonit_ad&password=5dbbef18256a11eebe560242ac120002&sender_number=9890006740&receiver_number=%s&note=%s'


def validate_phone_number(data: str):
    if not re.match(PHONE_NUMBER_REGEX, data):
        raise ValidationError('شماره تلفن همراه معتبر نمیباشد')
    return data


def send_otp_code(phone_number, code):
    try:
        api = SMS_API % (phone_number, f'{code} کد تایید شما ')
        response = requests.get(api)
        response_text = response.text
        if not response_text or 'error' in response_text:
            return False
        return response_text

    except Exception as e:
        print(e)
