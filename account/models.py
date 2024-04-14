from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='تلفن همراه')
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True, verbose_name='ایمیل')
    first_name = models.CharField(max_length=100, verbose_name='نام')
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    password = models.CharField(max_length=128, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.phone_number

    @property
    def is_staff(self):
        return self.is_admin

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
