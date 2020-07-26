from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField('手机号码', max_length=11, blank=True, null=True)
    avatar = models.IntegerField(default=0)

    class Meta:
        db_table = 'user'
