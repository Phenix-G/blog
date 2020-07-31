from rest_framework.views import APIView
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import User
from .serializers import UserDetailSerializer, UserEmailRegisterSerializer

from utils.permissions import IsOwnerOrReadOnly


class CustomBackend(ModelBackend):
    """
    自定义用户验证:
        用户名登录 手机号登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(email=username))
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
            return UserEmailRegisterSerializer
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
        # payload = jwt_payload_handler(user)
        # re_dict['token'] = jwt_encode_handler(payload)
        # re_dict['name'] = user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    # 返回当前用户 /user/{id} id可以是任意值
    def get_object(self):
        return self.request.user


# 激活邮箱
class EmailVariyView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, token):
        # 进行解密,获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 5 * 60)
        token = token.split('/')[-1]
        try:
            info = serializer.loads(token)
            # 获取待激活用户的ID
            username = info['confirm']
            # 根据用户名获取用户信息
            user = User.objects.filter(username=username)[0]
            user.is_active = 1
            user.save()
            # 跳转到登录页面
        except Exception as e:
            # 激活链接已过期
            return Response('激活链接已过期', status=status.HTTP_400_BAD_REQUEST)
        return Response('用户已激活', status=status.HTTP_200_OK)
