# from rest_framework import permissions
# from user.models import User
#
#
# class UserPermission(permissions.BasePermission):
#     """
#     对列入黑名单的IP进行全局权限检查。
#     """
#
#     def has_permission(self, request, view):
#         username = request.META['username']
#         blacklisted = User.objects.filter(username=username).exists()
#         return blacklisted
