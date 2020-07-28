from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import User
from .serializers import UserDetailSerializer, UserRegisterSerializer

from utils.permissions import IsOwnerOrReadOnly


class CustomBackend(ModelBackend):
    """
    自定义用户验证:
        用户名登录 手机号登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(phone=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    用户
    retrieve:
            用户个人信息
    create:
            用户注册
    update:
            用户个人资料修改
    """
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_queryset(self):
        if self.action == 'retrieve':
            return User.objects.filter(username=self.request.user.username)
        elif self.action == 'create':
            return User.objects.all()
        return User.objects.filter(username=self.request.user.username)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegisterSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        elif self.action == 'create':
            return []
        return []

    # 用户注册并登录
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    # 返回当前用户 /user/{id} id可以是任意值
    def get_object(self):
        return self.request.user
