from django.db import models


class TimeStamp(models.Model):
    created_time = models.DateTimeField("创建时间", auto_now_add=True)
    updated_time = models.DateTimeField("修改时间", auto_now=True)

    class Meta:
        abstract = True


class Status(models.Model):
    STATUS_SHOW = 2
    STATUS_HIDE = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_SHOW, "展示"),
        (STATUS_HIDE, "隐藏"),
        (STATUS_DELETE, "删除"),
    ]
    status = models.PositiveIntegerField("状态", default=1, choices=STATUS_ITEMS)
    weight = models.PositiveIntegerField(
        "优先级", help_text="数值越大越靠前", choices=zip(range(1, 6), range(1, 6))
    )

    class Meta:
        abstract = True
