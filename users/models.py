# Create your models here.
from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):
    groups = None
    user_permissions = None
    creator = models.CharField('创建人', max_length=200, null=True)
    nickname = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    phone = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '账号管理'
        verbose_name = '账号管理'
        app_label = 'users'
