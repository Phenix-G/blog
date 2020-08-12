from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from user.serializers import CommentSerializer
from .models import Post, Category, Tag
from .serializers import PostRetrieveSerializer, PostListSerializer, CategorySerializer, TagSerializer


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:文章列表
    retrieve:文章详情
    """
    queryset = Post.objects.all()
    pagination_class = PostPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('category', 'tag',)
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

    @action(
        methods=["GET"],
        detail=True,
        url_path="comments",
        url_name="comment",
    )
    def list_comments(self, request, *args, **kwargs):
        # 根据 URL 传入的参数值（文章 id）获取到博客文章记录
        post = self.get_object()
        # 获取文章下关联的全部评论
        comment = post.comment_set.all().order_by("-created_time")
        # 对评论列表进行分页，根据 URL 传入的参数获取指定页的评论
        # 序列化评论
        serializer = CommentSerializer(comment, many=True)
        # 返回分页后的评论列表
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
