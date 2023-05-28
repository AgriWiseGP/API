from rest_framework import permissions


class IsChatMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id or obj.specialist.id == request.user.id
