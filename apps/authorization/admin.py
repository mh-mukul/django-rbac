from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Module, Permission, Role, RolePermission


@admin.register(Module)
class ModuleAdmin(ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'is_deleted', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


@admin.register(Permission)
class PermissionAdmin(ModelAdmin):
    list_display = ('id', 'name', 'codename', 'module', 'is_active', 'is_deleted',
                    'created_at')
    search_fields = ('name', 'codename', 'module__name')
    ordering = ('-created_at',)
    list_filter = ('module',)


@admin.register(Role)
class RoleAdmin(ModelAdmin):
    list_display = ('id', 'name', 'organization',
                    'editable', 'is_active', 'is_deleted', 'created_at')
    search_fields = ('name', 'organization__name')
    ordering = ('-created_at',)
    list_filter = ('organization', 'editable')


@admin.register(RolePermission)
class RolePermissionAdmin(ModelAdmin):
    list_display = ('id', 'role', 'permission', 'is_active', 'is_deleted',
                    'created_at')
    search_fields = ('role__name', 'permission__name', 'permission__codename')
    ordering = ('-created_at',)
    list_filter = ('role', 'permission__module')
