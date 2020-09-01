from django.db import models
from django.contrib.auth.models import AbstractUser
from blog.models import Post


class User(AbstractUser):
    # phone = models.CharField('手机号码', max_length=11, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
