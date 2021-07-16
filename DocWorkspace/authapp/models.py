from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager

class UserKind(models.Model):
    USER_KINDS = (
        ('D', 'Врач'),
        ('N', 'Медсетра'),
        ('L', 'Лаборант'),
    )
    kind = models.CharField('Вид деятельности', max_length=1, choices=USER_KINDS)

    class Meta:
        verbose_name = 'Вид деятельности'
        verbose_name_plural = 'Виды деятельности'
    
    def __str__(self):
        return self.get_kind_display()


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Логин', max_length=30, unique=True)
    full_name = models.CharField('ФИО', max_length=100)
    kind = models.ForeignKey(UserKind, verbose_name='Вид деятельности', on_delete=models.CASCADE, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def __str__(self):
        return self.full_name
