from django.db import models

from db.abstract_model import Status, TimeStamp


class Category(Status, TimeStamp):
    name = models.CharField("分类", max_length=15)

    def __str__(self):
        return self.name


class Tag(Status, TimeStamp):
    name = models.CharField("标签", max_length=15)

    def __str__(self):
        return self.name


class Article(Status, TimeStamp):
    title = models.CharField("标题", max_length=20)
    view = models.PositiveIntegerField("阅读数", default=0, editable=False)
    desc = models.CharField("摘要", max_length=200, blank=True)
    content = models.TextField("文章内容")
    like = models.PositiveIntegerField("点赞数", default=0, editable=False)
    collect = models.PositiveIntegerField("收藏数", default=0, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET(""), verbose_name="分类")
    tag = models.ManyToManyField(Tag, blank=True, verbose_name="标签")

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return self.title
