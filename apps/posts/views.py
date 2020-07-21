from rest_framework import viewsets

from .serializers import PostsSerializer
from .models import Posts


class PostsViewSet(viewsets.ModelViewSet):
    serializer_class = PostsSerializer
    queryset = Posts.objects.all()
