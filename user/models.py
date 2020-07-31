from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # phone = models.CharField('手机号码', max_length=11, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'user'
