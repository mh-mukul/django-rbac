from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('mobile',
                    'is_active', 'is_staff', 'is_superuser', 'is_deleted')
    search_fields = ('mobile',)
    ordering = ('-id',)

    fieldsets = (
        (None, {'fields': ('mobile', 'password')}),
        ('Personal info', {'fields': ('name', 'email')}),
        ('Permissions', {'fields': ('is_active',
         'is_admin', 'is_staff', 'is_superuser', 'is_deleted')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'password1', 'password2'),
        }),
    )
