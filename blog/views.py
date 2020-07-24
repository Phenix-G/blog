from rest_framework import mixins, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Post, Category, Tag
from .serializers import PostRetrieveSerializer, PostListSerializer, CategorySerializer, TagSerializer


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:文章列表
    retrieve:文章详情
    """
    queryset = Post.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('category', 'tag',)
    ordering_fields = ('created_time',)
    search_fields = ['title', 'content', 'excerpt']

    # 文章阅读数
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        instance.increase_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        if self.action == 'retrieve':
            return PostRetrieveSerializer


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
