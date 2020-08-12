import re
from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from itsdangerous import TimedJSONWebSignatureSerializer

from blog.serializers import PostListSerializer, PostRetrieveSerializer
from .models import User, Comment
from blog.models import Post
from utils.email import send_register_active_email


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    username = serializers.CharField(required=False, label='密码', help_text='密码', read_only=True)

    email = serializers.EmailField(required=False, label='邮箱', help_text='邮箱', read_only=True)

    password = serializers.CharField(required=True, label='密码', help_text='密码', write_only=True)
    check_password = serializers.CharField(required=True, label='确认密码', help_text='确认密码', write_only=True)

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        password = validated_data.get('password', instance.password)
        check_password = validated_data.get('check_password', instance.check_password)

        if password == check_password:
            instance.set_password(password)
            instance.save()
        else:
            raise serializers.ValidationError('密码不一致')
        return instance

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'check_password'
        ]


# class UserRegisterSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(required=True, label='用户名', help_text='用户名', max_length=10,
#                                      validators=[UniqueValidator(queryset=User.objects.all(), message='用户名已存在')]
#                                      )
#     # phone = serializers.CharField(required=True, label='手机号码', help_text='手机号码', max_length=11, min_length=11,
#     #                               validators=[UniqueValidator(queryset=User.objects.all(), message='手机号码已存在')]
#     #                               )
#
#     email = serializers.EmailField(required=False, label='邮箱', help_text='邮箱',
#                                    validators=[UniqueValidator(queryset=User.objects.all(), message='邮箱已存在')]
#                                    )
#     password = serializers.CharField(
#         label='密码', help_text='密码', write_only=True,
#     )
#
#     # 创建用户设置密码
#     def create(self, validated_data):
#         user = super().create(validated_data)
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
#
#     class Meta:
#         model = User
#         fields = ("username", 'password', 'email')


class UserEmailRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, label='用户名', help_text='用户名', max_length=15,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户名已存在')]
                                     )

    email = serializers.EmailField(required=True, label='邮箱', help_text='邮箱',
                                   # validators=[UniqueValidator(queryset=User.objects.all(), message='邮箱已存在')]
                                   )

    password = serializers.CharField(required=True, label='密码', help_text='密码', write_only=True)
    check_password = serializers.CharField(required=True, label='确认密码', help_text='确认密码', write_only=True)

    def validate(self, attrs):
        """
         整体验证
        :param attrs:
        :return:
        """
        password = attrs['password']
        check_password = attrs['check_password']
        if password != check_password:
            raise serializers.ValidationError('密码不一致')
        return attrs

    def validate_email(self, email):
        """
        验证邮箱
        :param email:
        :return:
        """
        # 验证邮箱是否合法
        if not re.match(settings.REGEX_EMAIL, email):
            raise serializers.ValidationError('邮箱无效')

        # 邮箱是否注册
        if User.objects.filter(email=email).count():
            raise serializers.ValidationError('邮箱已注册')

        # 验证发码送频率
        # one_mintes_age = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        # if VerifyCode.objects.filter(add_time__gt=one_mintes_age, mobile=mobile).count():
        #     raise serializers.ValidationError('距离上一次发送未超过60s')
        return email

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        user = User.objects.create(username=username, password=password, email=email)

        # 设置用户密码
        user.set_password(password)
        user.save()
        # 发送邮箱激活邮件
        send_register_active_email(email)
        return user


class CommentSerializer(serializers.ModelSerializer):
    # 获取当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    username = serializers.ReadOnlyField(source='user.username')
    post_title = serializers.ReadOnlyField(source='post.title')
    # 只返回时间不提交
    created_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Comment
        fields = [
            'user',
            'username',
            'post',
            'post_title',
            'text',
            'created_time'
        ]
        # read_only_fields = [
        #     "created_time",
        # ]
        # extra_kwargs = {"post": {"write_only": True}}
