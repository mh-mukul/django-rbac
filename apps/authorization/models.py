from django.db import models
from apps.core.models import AbstractBaseFields

from apps.organization.models import Organization


class Module(AbstractBaseFields):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "modules"

    def __str__(self):
        return self.name


class Permission(AbstractBaseFields):
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=100, unique=True)
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="permissions")

    class Meta:
        db_table = "permissions"

    def __str__(self):
        return self.name


class Role(AbstractBaseFields):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="roles")
    editable = models.BooleanField(default=True)

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.name


class RolePermission(AbstractBaseFields):
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="role_permissions")
    permission = models.ForeignKey(
        Permission, on_delete=models.CASCADE, related_name="permission_roles")

    class Meta:
        db_table = "role_permissions"

    def __str__(self):
        return f"{self.role.name} - {self.permission.codename}"
