import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + '../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

import django

django.setup()

from random import randint
from faker import Faker

from apps.tag.models import Tag
from apps.posts.models import Posts
from apps.category.models import Category

faker = Faker('zh-CN')

# for i in range(10):
#     category = Category.objects.create(name=faker.word())
#     tag = Tag.objects.create(name=faker.word())

for i in range(10):
    title = faker.word()
    category = Category.objects.filter(id=randint(0, 20))
    content = faker.sentence(50)
    tag = Tag.objects.filter(id=randint(0, 20))
    post = Posts.objects.create(title=title, category=category[0], content=content, tag=tag[0])
