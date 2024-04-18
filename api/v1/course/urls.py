from django.urls import path
from rest_framework.routers import SimpleRouter
from .apis import CourseViewSet, CategoryViewSet, CreateAuthor

router = SimpleRouter()
router.register(prefix='', viewset=CourseViewSet, basename='course')
router.register(prefix='category', viewset=CategoryViewSet, basename='category')

app_name = 'course'

urlpatterns = [
                  path('author/', CreateAuthor.as_view(), name='author_create')
              ] + router.urls
