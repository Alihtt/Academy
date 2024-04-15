from django.urls import path
from .apis import Login, LoginVerify

app_name = 'account'

urlpatterns = [
    path('', Login.as_view(), name='register'),
    path('verify/', LoginVerify.as_view(), name='register-verify'),

]
