from django.db import models
from db.abstract_model import TimeStamp


# Create your models here.


class Comics(models.Model):
    unique_id = models.IntegerField('漫威ID')
    title = models.CharField('标题', max_length=255)
    description = models.CharField('描述', max_length=255)
    modified = models.DateTimeField('漫威修改时间', auto_now=True)
    text = models.TextField(verbose_name='漫画文本描述')
    resource_url = models.URLField('链接')
    public_url = models.URLField('公共网站链接')

class Creator:
    pass


class Event:
    pass


class Series:
    pass


class Story:
    pass


class Character(models.Model):
    name = models.CharField('角色名字', max_length=20)
    description = models.CharField('角色描述', max_length=255)
    comics = models.ManyToManyField(Comics, verbose_name='漫画')
    series = models.ManyToManyField(Series, verbose_name='系列')
    story = models.ManyToManyField(Story, verbose_name='故事')
    event = models.ManyToManyField(Event, verbose_name='事件')


class Image(models.Model):
    url = models.URLField('图片链接')
    extension = models.CharField('图片拓展名')
