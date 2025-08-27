from rest_framework import serializers
from apps.authorization.models import Module, Permission, Role, RolePermission


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["id", "name", "created_at"]
        read_only_fields = ["id", "created_at"]


class PermissionSerializer(serializers.ModelSerializer):
    module = ModuleSerializer(read_only=True)

    class Meta:
        model = Permission
        fields = ["id", "name", "codename",
                  "module", "created_at"]
        read_only_fields = ["id", "created_at"]


class PermissionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "codename", "module"]
        read_only_fields = ["id",]


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(
        source='get_permissions', many=True, read_only=True)

    class Meta:
        model = Role
        fields = ["id", "name", "description", "organization",
                  "editable", "permissions", "created_at"]
        read_only_fields = ["id", "created_at"]


class RoleCreateUpdateSerializer(serializers.ModelSerializer):
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Role
        fields = ["id", "name", "description", "editable", "permission_ids"]
        read_only_fields = ["id",]

    def create(self, validated_data):
        permission_ids = validated_data.pop('permission_ids', [])
        role = Role.objects.create(**validated_data)
        for perm_id in permission_ids:
            try:
                permission = Permission.objects.get(id=perm_id)
                RolePermission.objects.create(role=role, permission=permission)
            except Permission.DoesNotExist:
                continue
        return role

    def update(self, instance, validated_data):
        permission_ids = validated_data.pop('permission_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if permission_ids is not None:
            instance.role_permissions.all().delete()
            for perm_id in permission_ids:
                try:
                    permission = Permission.objects.get(id=perm_id)
                    RolePermission.objects.create(
                        role=instance, permission=permission)
                except Permission.DoesNotExist:
                    continue
        return instance
