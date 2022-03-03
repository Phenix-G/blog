import json

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from myblog.settings.base import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

from .models import User
from .serializers import (
    TirdPartyLoginSerializer,
    UserDetailSerializer,
    UserRegisterSerializer,
)


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


class UserActive(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        user.is_active = True
        user.save()
        return HttpResponseRedirect("https://github.com")


class ThirdPartyLogin(GenericViewSet):
    serializer_class = TirdPartyLoginSerializer

    @action(detail=False, methods=["get"])
    def github(self, request):
        code = request.GET.get("code")
        access_token = self.get_token(code)
        data = self.get_user_info(access_token)
        user, created = User.objects.filter(username=data["username"]).get_or_create(
            username=data["username"], is_active=True
        )
        return Response({"result": "success"})

    def get_token(self, code):
        headers = {"Accept": "application/json"}
        url = "https://github.com/login/oauth/access_token"
        body = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
        }
        response = requests.post(url=url, data=body, headers=headers)
        data = json.loads(response.text)
        return data.get("access_token")

    def get_user_info(self, token):
        headers = {"Authorization": f"token {token}"}
        url = "https://api.github.com/user"
        response = requests.get(url=url, headers=headers)
        data = json.loads(response.text)
        re_dict = {
            "username": data["login"],
            "avatar": data["avatar_url"],
            "email": data["email"],
        }
        return re_dict
