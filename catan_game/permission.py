from rest_framework.permissions import BasePermission
from . import models
from rest_framework.views import APIView

# permission_active = True
permission_active = False


#
#
# permission_active = False


class TestPermission(BasePermission):

    def has_permission(self, request, view):
        if not permission_active:
            return True
        return True

    def has_object_permission(self, request, view, obj):
        if not permission_active:
            return True
        return False


class IsInCatanEvent(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class IsUserTurn(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        obj: models.CatanEvent
        if not permission_active:
            return True
        if obj.turn == request.user:
            return True
        return False
