from django.db import models
from account.models import User


class Category(models.Model):
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='categories', null=True, blank=True, verbose_name='زیر مجموعه')
    is_child = models.BooleanField(default=False, verbose_name='زیر مجموعه است؟')
    name = models.CharField(max_length=200, verbose_name='نام')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='اسلاگ')

    class Meta:
        ordering = ('name',)
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name


def author_directory_path(instance, image_name):
    return 'authors/{0}/{1}'.format(instance.id, image_name)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author', verbose_name='کاربر', null=True)
    name = models.CharField(max_length=200, verbose_name='نام و نام خانوادگی')
    bio = models.TextField(verbose_name='بایوگرافی', default='')
    image = models.ImageField(verbose_name='تصویر', upload_to=author_directory_path, null=True, blank=True)
    social_link = models.CharField(max_length=100, verbose_name='آدرس فضای مجازی', null=True, blank=True)

    class Meta:
        verbose_name = 'استاد'
        verbose_name_plural = 'استادان'

    def __str__(self):
        return self.name


def course_directory_path(instance, image_name):
    return 'courses/{0}/{1}/{2}'.format(instance.author.id, instance.slug, image_name)


class Course(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='courses', verbose_name='استاد')
    category = models.ManyToManyField(Category, related_name='courses',
                                      verbose_name='دسته بندی')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='اسلاگ')
    image = models.ImageField(verbose_name='تصویر', upload_to=course_directory_path)
    price = models.PositiveIntegerField(verbose_name='قیمت')
    description = models.TextField(verbose_name='توضیحات')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره ها'
        ordering = ('-created',)

    def __str__(self):
        return self.title


class File(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='files', verbose_name='دوره')
    file = models.FileField(verbose_name='فایل')
    is_free = models.BooleanField(verbose_name='رایگان')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'فایل'
        verbose_name_plural = 'فایل ها'
        ordering = ('created',)

    def __str__(self):
        return f'{self.course} - {self.file.name}'
