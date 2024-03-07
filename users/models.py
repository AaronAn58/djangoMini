# Create your models here.
from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '账号管理'
        verbose_name = '账号管理'
        app_label = 'users'
