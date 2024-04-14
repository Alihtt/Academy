from django.urls import path
from .apis import RegisterUserSendCode, RegisterUserSendCodeDone

app_name = 'account'

urlpatterns = [
    path('', RegisterUserSendCode.as_view(), name='register'),
    path('verify/', RegisterUserSendCodeDone.as_view(), name='register-verify'),

]
