# Third-Party Libraries
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwner(BasePermission):
    message = "You must be the owner of this object."

    def has_object_permission(self, request, view, obj):
        return (
            True
            if request.method in SAFE_METHODS
            else obj.owner == request.user
        )


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of this object."

    def has_object_permission(self, request, view, obj):
        return (
            True
            if request.method in SAFE_METHODS
            else obj.owner == request.user
        )
