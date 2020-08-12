import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + '../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')

import django

django.setup()

from random import randint
from faker import Faker

from blog.models import Category, Post, Tag

faker = Faker('zh-CN')

for i in range(10):
    category = Category.objects.create(name=faker.word())
    tag = faker.words()
    for j in tag:
        Tag.objects.create(name=j)

for i in range(20):
    title = faker.word()
    category = Category.objects.order_by('?').first()
    content = faker.text(500)
    tag = Tag.objects.order_by('?')
    tag1 = tag.first()
    tag2 = tag.last()
    post = Post.objects.create(title=title, category=category, content=content)
    post.tag.add(tag1, tag2)
    post.save()
