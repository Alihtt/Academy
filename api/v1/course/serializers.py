from rest_framework import serializers
from course.models import Course, Category, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('category', 'title', 'slug', 'image', 'price', 'description')

    def create(self, validated_data):
        author = self.context['request'].user
        if author.status == 2:
            course = Course(author=author, **validated_data)
            course.save()
            return course
        raise serializers.ValidationError({'message': 'You must be author'})


class ChildCategorySerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        serializer_related_field = serializers.StringRelatedField()
        model = Category
        fields = '__all__'

    def get_course(self, obj):
        courses = obj.courses.all()
        return CourseSerializer(courses, many=True).data


class ParentCategorySerializer(serializers.ModelSerializer):
    child_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_child_category(self, obj):
        categories = obj.categories.all()
        return ChildCategorySerializer(categories, many=True).data
