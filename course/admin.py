from django.contrib import admin
from .models import Course, Category, Author, File


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'author', 'price', 'created')
    list_filter = ('created',)
    raw_id_fields = ('author', 'category')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'is_sub', 'sub_category')
    list_filter = ('name', 'is_sub')
    raw_id_fields = ('sub_category',)


admin.site.register(Author)
admin.site.register(File)
