from django.db import models

from apps.tag.models import Tag
from apps.category.models import Category


class Posts(models.Model):
    title = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    navigation = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    # is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'post'
