from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(verbose_name='بایوگرافی')
    image = models.ImageField(verbose_name='تصویر')
    social_link = models.CharField(max_length=100, verbose_name='آدرس فضای مجازی')

    class Meta:
        verbose_name = 'استاد'
        verbose_name_plural = 'استادان'

    def __str__(self):
        return f''


class Course(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='acourses', verbose_name='استاد')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='اسلاگ')
    image = models.ImageField(verbose_name='تصویر')
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
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cfiles', verbose_name='دوره')
    file = models.FileField(verbose_name='فایل')
    is_free = models.BooleanField(verbose_name='رایگان')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'فایل'
        verbose_name_plural = 'فایل ها'
        ordering = ('created',)

    def __str__(self):
        return f'{self.course} - {self.file.name}'
