from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import UserDetailSerializer, UserRegisterSerializer


class UserViewSet(GenericViewSet, CreateModelMixin):
    def get_queryset(self):
        if self.action == "create":
            queryset = User.objects.all()
        else:
            queryset = []
        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            serializer_class = UserRegisterSerializer
        else:
            serializer_class = UserDetailSerializer
        return serializer_class

    def get_permissions(self):
        if self.action == "create":
            permission = [AllowAny()]
        else:
            permission = [IsAuthenticated()]
        return permission

    @action(detail=False, methods=["get"])
    def profile(self, request):
        user = User.objects.filter(username=self.request.user.username)
        if user.exists():
            serializer = self.get_serializer(user[0]).data
        else:
            serializer = {}
        return Response(serializer)

    @action(detail=False, methods=["put"])
    def put(self, request):
        serializer = UserDetailSerializer(instance=self.request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
