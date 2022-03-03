from rest_framework import serializers

from utils.email import send_register_active_email

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        label="确认密码", write_only=True, style={"input_type": "password"}
    )

    def validate(self, attrs):
        password = attrs["password"]
        confirm_password = attrs["confirm_password"]
        if password == confirm_password:
            attrs.pop("confirm_password")
            return attrs
        else:
            raise serializers.ValidationError("密码不一致")

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        email = validated_data["email"]
        instance = User.objects.create_user(
            username=username, password=password, email=email
        )
        send_register_active_email(email, username)
        return instance

    class Meta:
        model = User
        fields = ["username", "password", "confirm_password", "email"]
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
            "email": {"required": True},
        }


class UserDetailSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        label="确认密码", write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["username", "email", "is_active", "confirm_password", "password"]
        read_only_fields = ["is_active"]
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def update(self, instance, validated_data):
        password = validated_data["password"]
        confirm_password = validated_data["confirm_password"]

        if password == confirm_password:
            instance.set_password(password)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError("密码不一致")


class TirdPartyLoginSerializer(serializers.Serializer):
    pass
