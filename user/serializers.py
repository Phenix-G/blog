import re

from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from utils.email import send_register_active_email, send_reset_password_email
from .models import User


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


class EmailActiveSerializer(serializers.Serializer):
    email = serializers.EmailField()

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
        user = User.objects.filter(email=email)[0]
        if user:
            if user.is_active:
                raise serializers.ValidationError('邮箱已激活')
            else:
                return email
        else:
            raise serializers.ValidationError('用户不存在')

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.get(email=email)
        send_register_active_email(email)
        return user


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

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
        if User.objects.filter(email=email):
            return email
        else:
            raise serializers.ValidationError('用户不存在')

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.get(email=email)

        # 发送重置密码邮件 设置用户密码
        user.set_password(send_reset_password_email(email))
        user.save()
        return user
