from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.organization.models import Organization


@admin.register(Organization)
class OrganizationAdmin(ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at',)
