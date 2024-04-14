from celery import shared_task
from .utils import send_otp_code


@shared_task()
def send_otp_task(phone_number, code):
    return send_otp_code(phone_number, code)
