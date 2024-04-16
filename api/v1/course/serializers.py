from rest_framework import serializers
from course.models import Course, Category


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


class SubCategorySerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        serializer_related_field = serializers.StringRelatedField()
        model = Category
        fields = '__all__'

    def get_course(self, obj):
        courses = obj.ccourse.all()
        return CourseSerializer(courses, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_sub_category(self, obj):
        categories = obj.scategory.all()
        return SubCategorySerializer(categories, many=True).data

    def get_course(self, obj):
        courses = obj.ccourse.all()
        return CourseSerializer(courses, many=True).data
