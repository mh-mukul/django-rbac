"""
Custom permission classes for the users app.
"""

from rest_framework import permissions


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Allow users to edit their own profile.
    Admins can edit anyone's profile.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow if admin user
        if request.user.is_staff:
            return True

        # Allow if object is the user
        return obj.pk == request.user.pk


class HasRolePermission(permissions.BasePermission):
    """
    Custom permission to check if a user has a specific role permission.

    Example usage:
    permission_classes = [HasRolePermission('user_create')]
    """

    def __init__(self, codename):
        self.codename = codename

    def has_permission(self, request, view):
        # Superuser is allowed
        if request.user.is_superuser:
            return True

        # Check if user has the permission
        return request.user.has_permission(self.codename)
