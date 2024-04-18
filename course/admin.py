from django.contrib import admin
from .models import Course, Category, Author, File


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'price', 'created')
    list_filter = ('created',)
    raw_id_fields = ('author',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'is_child', 'parent_category')
    list_filter = ('name', 'is_child')
    raw_id_fields = ('parent_category',)


admin.site.register(Author)
admin.site.register(File)
