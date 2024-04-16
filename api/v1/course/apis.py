from rest_framework import viewsets
from .serializers import CourseSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAuthorOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from course.models import Category
from api.pagination import StandardResultsSetPagination


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_sub=False)
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination


class CourseViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        serializer_classes = {
            "create": CourseSerializer,
        }
        return serializer_classes[self.action]

    def create(self, request):
        serializer = self.get_serializer_class()
        ser_data = serializer(data=request.data)
        if ser_data.is_valid():
            print(ser_data.data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
