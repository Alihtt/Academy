from django.urls import path, include
from .account.apis import UserViewSet
from rest_framework.routers import SimpleRouter

app_name = 'v1'
router = SimpleRouter()
router.register(r'account', UserViewSet, basename='account')

urlpatterns = [
    
]
urlpatterns += router.urls
