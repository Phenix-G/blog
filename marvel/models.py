from django.db import models

from db.abstract_model import TimeStamp


# Create your models here.
class BaseMarvel(TimeStamp):
    unique_id = models.IntegerField("漫威ID", db_index=True)
    description = models.CharField("描述", max_length=255)
    modified = models.DateTimeField("漫威修改时间", auto_now=True)
    thumbnail = models.URLField("缩略图链接")

    class Meta:
        abstract = True


class ResourceUri(models.Model):
    resource_uri = models.URLField("资源链接")

    class Meta:
        abstract = True


class PublicWebSite(models.Model):
    url = models.URLField("公共网站详情链接")
    type = models.CharField("类型", max_length=20)


class AbstractUrl(models.Model):
    url = models.ManyToManyField(PublicWebSite, verbose_name="公共网站详情链接")

    class Meta:
        abstract = True


class MarvelModel(BaseMarvel, ResourceUri):
    class Meta:
        abstract = True


class Variant(ResourceUri):
    name = models.CharField("名字", max_length=255)


class CharacterItem(ResourceUri):
    name = models.CharField("人物名字", max_length=255)


class ComicsItem(ResourceUri):
    name = models.CharField("漫画名称", max_length=255)


class CreatorItem(ResourceUri):
    name = models.CharField("创作者名字", max_length=255)
    role = models.CharField("角色", max_length=255)


class SeriesItem(ResourceUri):
    name = models.CharField("系列标题", max_length=255)


class StoryItem(ResourceUri):
    name = models.CharField("故事标题", max_length=255)
    type = models.CharField("类型", max_length=255)


class EventItem(ResourceUri):
    name = models.CharField("事件标题", max_length=255)


class AbstractComics(models.Model):
    comics = models.ManyToManyField(ComicsItem, verbose_name="漫画")

    class Meta:
        abstract = True


class AbstractSeries(models.Model):
    series = models.ManyToManyField(SeriesItem, verbose_name="系列")

    class Meta:
        abstract = True


class AbstractCreator(models.Model):
    creator = models.ManyToManyField(CreatorItem, verbose_name="创作者")

    class Meta:
        abstract = True


class AbstractStory(models.Model):
    story = models.ManyToManyField(StoryItem, verbose_name="故事")

    class Meta:
        abstract = True


class AbstractEvent(models.Model):
    event = models.ManyToManyField(EventItem, verbose_name="事件")

    class Meta:
        abstract = True


class AbstractCharacters(models.Model):
    character = models.ManyToManyField(CharacterItem, verbose_name="角色")

    class Meta:
        abstract = True


class Image(models.Model):
    path = models.URLField("图片链接")
    extension = models.CharField("图片拓展名", max_length=255)


class Character(
    MarvelModel,
    AbstractUrl,
    AbstractComics,
    AbstractSeries,
    AbstractStory,
    AbstractEvent,
):
    name = models.CharField("角色名字", max_length=20)

    def __str__(self):
        return self.name


class Comics(
    MarvelModel,
    AbstractUrl,
    AbstractSeries,
    AbstractCreator,
    AbstractCharacters,
    AbstractStory,
    AbstractEvent,
):
    title = models.CharField("漫画名称", max_length=255)
    description_text = models.TextField(verbose_name="漫画文本描述")
    variant = models.ManyToManyField(Variant, verbose_name="问题")
    image = models.ManyToManyField(Image, verbose_name="图片")


class Creator(
    MarvelModel,
    AbstractUrl,
    AbstractSeries,
    AbstractStory,
    AbstractComics,
    AbstractEvent,
):
    full_name = models.CharField("全名", max_length=255)
    suffix = models.CharField("荣誉", max_length=255)


class Event(
    MarvelModel,
    AbstractUrl,
    AbstractComics,
    AbstractStory,
    AbstractSeries,
    AbstractCharacters,
    AbstractCreator,
):
    title = models.CharField("事件标题", max_length=255)


class Series(
    MarvelModel,
    AbstractUrl,
    AbstractComics,
    AbstractStory,
    AbstractEvent,
    AbstractCharacters,
    AbstractCreator,
):
    title = models.CharField("系列名称", max_length=255)
    rating = models.CharField("年龄适用等级", max_length=255)


class OriginalIssue(ResourceUri):
    name = models.CharField(max_length=255)


class Story(
    MarvelModel,
    AbstractComics,
    AbstractSeries,
    AbstractEvent,
    AbstractCharacters,
    AbstractCreator,
):
    title = models.CharField("故事标题", max_length=255)
    type = models.CharField("故事类型", max_length=255)
    original_issue = models.ManyToManyField(OriginalIssue, verbose_name="故事原因")
