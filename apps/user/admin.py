from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # 🔧 Use Unfold's forms so the password field renders with the link
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ('mobile', 'is_active', 'is_staff',
                    'is_superuser', 'is_deleted')
    search_fields = ('mobile',)
    ordering = ('-id',)

    fieldsets = (
        (None, {'fields': ('mobile', 'password')}),   # keep `password` here
        ('Personal info', {
         'fields': ('name', 'email', 'organization', 'image')}),
        ('Permissions', {'fields': ('role', 'is_active',
         'is_admin', 'is_staff', 'is_superuser', 'is_deleted')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'password1', 'password2'),
        }),
    )
