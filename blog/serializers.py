from rest_framework import serializers

from blog.models import Article, Category, Tag


class TagSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="tag-detail")

    class Meta:
        model = Tag
        exclude = ["created_time", "updated_time"]


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="category-detail")

    class Meta:
        model = Category
        exclude = ["created_time", "updated_time"]


class ArticleDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    tag = TagSerializer(many=True)

    class Meta:
        model = Article
        exclude = ["content"]


class ArticleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    tag = TagSerializer(many=True)
    url = serializers.HyperlinkedIdentityField(view_name="article-detail")

    class Meta:
        model = Article
        exclude = ["content"]


class CategoryDetailSerializer(serializers.ModelSerializer):
    article_set = ArticleDetailSerializer(many=True)

    class Meta:
        model = Category
        fields = ["name", "article_set", "status"]


class TagDetailSerializer(serializers.ModelSerializer):
    article_set = ArticleListSerializer(many=True)

    class Meta:
        model = Category
        fields = ["name", "article_set", "status"]
