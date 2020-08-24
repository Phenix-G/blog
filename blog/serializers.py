from rest_framework import serializers

from .models import Category, Tag, Post


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()

    def get_post(self, obj):
        post = Post.objects.filter(category__id=obj.id)
        serializers_post = PostRetrieveSerializer(post, many=True)
        return serializers_post.data

    class Meta:
        model = Category
        fields = '__all__'


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagRetrieveSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()

    def get_post(self, obj):
        post = Post.objects.filter(tag__id=obj.id)
        serializers_post = PostRetrieveSerializer(post, many=True)
        return serializers_post.data

    class Meta:
        model = Tag
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    category = CategoryListSerializer()
    tag = TagListSerializer(many=True)

    class Meta:
        model = Post
        exclude = ['content']


class PostRetrieveSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    category = CategoryListSerializer()
    tag = TagListSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'
