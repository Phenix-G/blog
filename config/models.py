from django.db import models

from db.abstract_model import Status, TimeStamp


# Create your models here.
class FriendLink(Status, TimeStamp):
    name = models.CharField("标题", max_length=15)
    url = models.URLField()
    desc = models.CharField("描述", max_length=50)

    def __str__(self):
        return self.name


class SideBar(Status, TimeStamp):
    DISPLAY_LATEST = 1
    DISPLAY_HOT = 2
    DISPLAY_COMMENT = 3
    DISPLAY_COLLECT = 4
    DISPLAY_LIKE = 5
    DISPLAY_VIEW = 6
    DISPLAY_ITEMS = [
        (DISPLAY_LATEST, "最新文章"),
        (DISPLAY_HOT, "最热文章"),
        (DISPLAY_COMMENT, "评论最多"),
        (DISPLAY_COLLECT, "收藏最多"),
        (DISPLAY_LIKE, "点赞最多"),
        (DISPLAY_VIEW, "阅读数最多"),
    ]

    POSITION_LEFT = True
    POSITION_RIGHT = False
    POSITION_ITEMS = [
        (POSITION_LEFT, "左边"),
        (POSITION_RIGHT, "右边"),
    ]
    title = models.CharField("标题", max_length=50)
    display_type = models.PositiveIntegerField("展示类型", default=1, choices=DISPLAY_ITEMS)
    content = models.CharField("内容", max_length=200, blank=True)
    position = models.BooleanField("位置", default=POSITION_RIGHT, choices=POSITION_ITEMS)

    def __str__(self):
        return self.title
