from django.urls import path
from rest_framework.routers import SimpleRouter
from .apis import CourseViewSet, CategoryViewSet

router = SimpleRouter()
router.register(prefix='', viewset=CourseViewSet, basename='course')
router.register(prefix='category', viewset=CategoryViewSet, basename='category')

app_name = 'course'

urlpatterns = [

              ] + router.urls
