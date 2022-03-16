import hashlib
import json
import time
from pprint import pprint

import requests
from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from myblog.settings.base import Marvel_PRIVATE_KEY, Marvel_PUBLIC_KEY
from services.marvel.marvel import Marvel

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


class MarvelView(APIView):
    # def get(self, request):
    #     base_url = "http://gateway.marvel.com/"
    #     # Marvel_PUBLIC_KEY
    #     # Marvel_PRIVATE_KEY
    #     ts = str(int(time.time()))
    #
    #     hash_str = hashlib.md5(
    #         (ts + Marvel_PRIVATE_KEY + Marvel_PUBLIC_KEY).encode("utf8")
    #     ).hexdigest()
    #     params = {"ts": ts, "apikey": Marvel_PUBLIC_KEY, "hash": hash_str, "offset": 60}
    #     pprint(params)
    #     response = requests.get(url=base_url + "/v1/public/characters", params=params)
    #     data = json.loads(response.text)
    #     name_list = map(lambda x: x["name"], data["data"]["results"])
    #     return Response(data)
    def get(self, request):
        marvel = Marvel(Marvel_PRIVATE_KEY, Marvel_PUBLIC_KEY)
        data = marvel.characters.get("1011334")
        return Response(data)
