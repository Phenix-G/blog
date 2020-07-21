from rest_framework import mixins
from rest_framework import viewsets

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                 mixins.ListModelMixin, mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
