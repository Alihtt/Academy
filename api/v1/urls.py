from django.urls import path
from .account.apis import UserViewSet, ForgotPasswordView
from rest_framework.routers import SimpleRouter

app_name = 'v1'
router = SimpleRouter()
router.register(r'account', UserViewSet, basename='account')

urlpatterns = [
    path('account/forgot_password/', ForgotPasswordView.as_view(), name='forgot-password'),
]
urlpatterns += router.urls
