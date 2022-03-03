from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Article, Category, Tag
from .serializers import (
    ArticleListSerializer,
    CategoryDetailSerializer,
    CategorySerializer,
    TagDetailSerializer,
    TagSerializer,
)


class ArticleViewSet(ReadOnlyModelViewSet):
    serializer_class = ArticleListSerializer

    def get_queryset(self):
        if self.action == "list":
            queryset = (
                Article.objects.prefetch_related("tag")
                .select_related("category")
                .defer("content", "updated_time")
            )
        elif self.action == "retrieve":
            queryset = Article.objects.prefetch_related("tag").select_related(
                "category"
            )
        else:
            queryset = []
        return queryset


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.defer("created_time", "updated_time")

    def get_serializer_class(self):

        if self.action == "retrieve":
            serializer_class = CategoryDetailSerializer
        else:
            serializer_class = CategorySerializer
        return serializer_class


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.defer("created_time", "updated_time")

    def get_serializer_class(self):

        if self.action == "retrieve":
            serializer_class = TagDetailSerializer
        else:
            serializer_class = TagSerializer
        return serializer_class
