from django.conf import settings
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend

from rest_framework.views import APIView
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired

from utils.email import send_register_active_email
from .models import User, Comment
from .serializers import UserDetailSerializer, UserEmailRegisterSerializer, CommentSerializer, ResetPasswordSerializer

from utils.permissions import IsOwnerOrReadOnly


class CustomBackend(ModelBackend):
    """
    自定义用户验证:
        邮箱登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 用户
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
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

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
        return Response('激活邮件已发送到邮箱', status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    # 返回当前用户 /user/{id} id可以是任意值
    def get_object(self):
        return self.request.user


# 激活邮箱
class EmailActiveView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, token):
        # 进行解密,获取要激活的用户信息
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 5 * 60)
        token = token.split('/')[-1]
        try:
            info = serializer.loads(token)
            # 获取待激活用户的ID
            email = info['confirm'][18:]
            # 根据用户名获取用户信息
            user = User.objects.filter(email=email)[0]
            user.is_active = 1
            user.save()
            # 跳转到登录页面
        except SignatureExpired:
            # 激活链接已过期
            return Response('激活链接已过期', status=status.HTTP_400_BAD_REQUEST)
        return Response('用户已激活', status=status.HTTP_200_OK)


# 过期邮箱激活
class ExpireEmailActiveView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        email = request.POST.get('email')
        existed = User.objects.filter(email=email).count()
        if existed:
            if User.objects.filter(email=email)[0].is_active:
                return Response('邮箱已激活', status=status.HTTP_400_BAD_REQUEST)
            else:
                send_register_active_email(email)
                return Response('激活邮件已发送到你的邮箱,请在5分钟内激活账号', status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


# 重置密码
class ResetPassWord(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
    重置密码
    """
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response('密码已发送到邮箱', status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save()


# 评论
class CommentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
    发表评论
    """
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication]

    # 这里用了get_queryset来指定queryset 那么我们上面的query_set可以省略不写, 但是前提是在注册路由是需要加个base_name
    def get_queryset(self):
        # self.request.user 当前用户
        return Comment.objects.filter(user=self.request.user)
