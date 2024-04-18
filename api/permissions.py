from rest_framework import permissions
from course.models import Author


class IsAuthorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.status == 2:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user.author
