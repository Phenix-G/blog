from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import mixins, viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from .models import User
from .serializers import UserDetailSerializer, UserRegSerializer


class CustomBackend(ModelBackend):
    """
    自定义用户验证:
        用户名登录 手机号登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(phone=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


#
class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    # def get_queryset(self):
    #     return User.objects.filter(username=self.request.user.username)
    #
    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return UserDetailSerializer
    #     elif self.action == 'create':
    #         return UserRegSerializer
    #     return UserRegSerializer
    #
    # def get_permissions(self):
    #     if self.action == 'retrieve':
    #         return [IsAuthenticated()]
    #     elif self.action == 'create':
    #         return []
    #     return []
    queryset = User.objects.all()
    serializer_class = UserRegSerializer

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
