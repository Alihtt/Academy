# Generated by Django 5.0.4 on 2024-04-15 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('bio', models.TextField(verbose_name='بایوگرافی')),
                ('image', models.ImageField(upload_to='', verbose_name='تصویر')),
                ('social_link', models.CharField(max_length=100, verbose_name='آدرس فضای مجازی')),
            ],
            options={
                'verbose_name': 'استاد',
                'verbose_name_plural': 'استادان',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='اسلاگ')),
                ('image', models.ImageField(upload_to='', verbose_name='تصویر')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acourses', to='course.author', verbose_name='استاد')),
            ],
            options={
                'verbose_name': 'دوره',
                'verbose_name_plural': 'دوره ها',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='', verbose_name='فایل')),
                ('is_free', models.BooleanField(verbose_name='رایگان')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cfiles', to='course.course', verbose_name='دوره')),
            ],
            options={
                'verbose_name': 'فایل',
                'verbose_name_plural': 'فایل ها',
                'ordering': ('created',),
            },
        ),
    ]
