from django.db import models


class Category(models.Model):
    name = models.CharField('分类', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Category'


class Tag(models.Model):
    name = models.CharField('标签', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Tag'


class Post(models.Model):
    title = models.CharField('标题', max_length=50)
    created_time = models.DateTimeField('发布时间', auto_now_add=True)
    look = models.IntegerField('阅读数', default=0, editable=False)
    excerpt = models.CharField('摘录', max_length=200)
    content = models.TextField('文章内容')
    # navigation = models.CharField('导航',max_length=50)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='分类')
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='标签')

    def __str__(self):
        return self.title

    def increase_views(self):
        self.look += 1
        self.save(update_fields=["look"])

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.excerpt = self.content[:60]
        super().save()

    class Meta:
        db_table = 'Post'
        ordering = ['-created_time']
