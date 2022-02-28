from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_active = models.BooleanField("是否激活", default=False)

    def __str__(self):
        return self.username
