from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)

    class Meta(AbstractUser.Meta):
        pass


CustomUser._meta.get_field('user_permissions').related_name = 'custom_user_permissions'
CustomUser._meta.get_field('groups').related_name = 'custom_user_groups'
CustomUser._meta.get_field('user_permissions').related_name = 'custom_user_permissions'
CustomUser._meta.get_field('groups').related_name = 'custom_user_groups'
