from rest_framework import serializers

from .models import Posts

from apps.tag.serializers import TagSerializer
from apps.category.serializers import CategorySerializer


class PostsSerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    category = CategorySerializer()

    class Meta:
        model = Posts
        fields = "__all__"
