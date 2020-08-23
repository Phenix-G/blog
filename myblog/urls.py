"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

from blog.views import PostViewSet, TagViewSet, CategoryViewSet
from user.views import UserViewSet, ExpireEmailActiveView, EmailActiveView, ResetPassword, CommentViewSet

router = routers.DefaultRouter()

router.register(r'posts', PostViewSet, basename='post')
router.register(r'categorys', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'users', UserViewSet, basename='users')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title='我的博客')),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r'^login/', obtain_jwt_token),
    re_path(r'^active/(?P<token>.*)$', EmailActiveView.as_view()),  # 用户激活
    path('email_active/', ExpireEmailActiveView.as_view()),  # 邮箱过期激活
    path('reset_password/', ResetPassword.as_view())  # 重置密码
]
