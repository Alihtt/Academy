from rest_framework import viewsets
from .serializers import CourseSerializer, ParentCategorySerializer, AuthorSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.permissions import IsAuthorPermission
from rest_framework.response import Response
from rest_framework import status
from course.models import Category, Course
from rest_framework.views import APIView
from api.pagination import StandardResultsSetPagination


class CreateAuthor(APIView):
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated, IsAuthorPermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get(self, request):
        author = request.user.author
        ser_data = self.serializer_class(instance=author)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            ser_data.save(user=request.user)
            request.user.status = 2
            request.user.save()
            return Response({'message': 'با موفقیت ذخیره شد'}, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_child=False)
    serializer_class = ParentCategorySerializer
    pagination_class = StandardResultsSetPagination


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAuthorPermission]  # Default to authenticated for other actions
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        serializer_classes = {
            'list': CourseSerializer,
            "create": CourseSerializer,
        }
        return serializer_classes[self.action]

    def create(self, request):
        serializer = self.get_serializer_class()
        ser_data = serializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
