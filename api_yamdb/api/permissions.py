from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Checking user is admin."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_staff


class ReviewCommentPermission(permissions.BasePermission):
    """
    Checking permissions to create and edit records for:
    - user;
    - moderator;
    - admin.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Checking user is admin."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_admin or request.user.is_superuser:
                return True

        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_admin or request.user.is_superuser:
                return True

        return request.method in permissions.SAFE_METHODS


class ReadOnly(permissions.BasePermission):
    """Checking user is allowed to read only."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
