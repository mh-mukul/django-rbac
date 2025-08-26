from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access a view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_admin


class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow superusers to access a view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class HasRolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        required_permissions = getattr(view, 'required_permissions', None)

        if required_permissions and request.user.is_authenticated:
            user_permissions = request.user.get_all_permissions()
            return True if request.user.is_superuser or any(
                perm in user_permissions for perm in required_permissions
            ) else False
        return False
