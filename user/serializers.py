from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserDetailSerializer(serializers.ModelSerializer):
    # def update(self, instance, validated_data):
    #     """更新，instance为要更新的对象实例"""
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.phone = validated_data.get('phone', instance.phone)
    #     instance.save()
    #     return instance

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone'
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, label='用户名', help_text='用户名', max_length=10,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户名已存在')]
                                     )
    phone = serializers.CharField(required=True, label='手机号码', help_text='手机号码', max_length=11, min_length=11,
                                  validators=[UniqueValidator(queryset=User.objects.all(), message='手机号码已存在')]
                                  )

    password = serializers.CharField(
        label='密码', help_text='密码', write_only=True,
    )

    # 创建用户设置密码
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("username", 'password', 'phone')
