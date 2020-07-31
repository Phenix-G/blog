import re
from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from .models import User


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    # def update(self, instance, validated_data):
    #     """更新，instance为要更新的对象实例"""
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.phone = validated_data.get('phone', instance.phone)
    #     instance.save()
    #     return instance
    username = serializers.CharField(required=False, allow_blank=False, label='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户名已存在')])
    # phone = serializers.CharField(required=False, label='手机号码', help_text='手机号码', max_length=11, min_length=11,
    #                               validators=[UniqueValidator(queryset=User.objects.all(), message='手机号码已存在')]
    #                               )
    email = serializers.EmailField(required=False, label='邮箱', help_text='邮箱',
                                   validators=[UniqueValidator(queryset=User.objects.all(), message='邮箱已存在')]
                                   )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email',
            'is_active'
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
    username = serializers.CharField(required=True, label='用户名', help_text='用户名', max_length=10,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户名已存在')]
                                     )

    email = serializers.EmailField(required=False, label='邮箱', help_text='邮箱',
                                   validators=[UniqueValidator(queryset=User.objects.all(), message='邮箱已存在')]
                                   )
    password = serializers.CharField(
        label='密码', help_text='密码', write_only=True,
    )

    def validated_email(self, email):
        """
        验证邮箱
        :param email:
        :return:
        """
        # 邮箱是否注册
        if User.objects.filter(email=email).count():
            raise serializers.ValidationError('用户已经存在')
        # 验证手机号码是否合法
        if not re.match(settings.REGEX_EMAIL, email):
            raise serializers.ValidationError('邮箱无效')

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
        # 生成激活连接
        serializer = Serializer(settings.SECRET_KEY, 5 * 60)
        info = {'confirm': username}
        token = serializer.dumps(info)
        token = token.decode('utf8')

        # 加密
        url = 'http://127.0.0.1:8000/active/{}'.format(token)

        # todo 发送邮件
        # 邮件主题
        subject = '尚惠欢迎信息'
        # 邮件信息，正文部分
        message = '欢迎'
        # 发送者，直接从配置文件中导入上面配置的发送者
        sender = settings.EMAIL_FROM
        # 接收者的邮箱，是一个列表，这里是前端用户注册时传过来的 email
        receiver = [email]
        # html结构的信息，其中包含了加密后的用户信息token
        html_message = '<a href=' + url + '>' + url + '</a>'
        # 调用Django发送邮件的方法，这里传了5个参数
        send_mail(subject, message, sender, receiver, html_message=html_message)
        return user
