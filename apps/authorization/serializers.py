from rest_framework import serializers
from apps.authorization.models import Module, Permission, Role, RolePermission


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["id", "name", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        if Module.objects.filter(name=validated_data['name'], is_deleted=False).exists():
            raise serializers.ValidationError(
                {"name": ["Module with this name already exists."]})
        return Module.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data and Module.objects.filter(name=validated_data['name'], is_deleted=False).exclude(id=instance.id).exists():
            raise serializers.ValidationError(
                {"name": ["Module with this name already exists."]})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


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
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ["id", "name", "description", "organization",
                  "editable", "permissions", "created_at"]
        read_only_fields = ["id", "created_at"]

    def get_permissions(self, obj):
        permissions = obj.role_permissions.select_related('permission').filter(
            is_active=True, is_deleted=False)
        return PermissionSerializer([rp.permission for rp in permissions], many=True).data


class RoleCreateUpdateSerializer(serializers.ModelSerializer):
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Role
        fields = ["id", "name", "description", "editable", "permission_ids"]
        read_only_fields = ["id",]
    
    def validate(self, data):
        name = data.get('name')
        request = self.context.get('request')
        organization = None
        
        if request and hasattr(request, 'user'):
            organization = request.user.organization
        
        # For update operation
        if self.instance:
            if name and Role.objects.filter(
                name=name, 
                organization=self.instance.organization, 
                is_deleted=False
            ).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(
                    {"name": ["Role with this name already exists in this organization."]})
        # For create operation
        elif name and Role.objects.filter(
            name=name, 
            organization=organization, 
            is_deleted=False
        ).exists():
            raise serializers.ValidationError(
                {"name": ["Role with this name already exists in this organization."]})
        
        return data

    def create(self, validated_data):
        permission_ids = validated_data.pop('permission_ids', [])
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['organization'] = request.user.organization
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user
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
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['updated_by'] = request.user
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.role_permissions.update(is_active=False, is_deleted=True)
        for perm_id in (permission_ids or []):
            try:
                permission = Permission.objects.get(id=perm_id)
                RolePermission.objects.create(
                    role=instance, permission=permission)
            except Permission.DoesNotExist:
                continue

        return instance
