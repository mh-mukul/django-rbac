from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from apps.organization.models import Organization
from apps.authorization.models import Role, Permission


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile, password, **extra_fields):
        if not mobile:
            raise ValueError('The Phone must be set')
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(mobile, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=40)
    mobile = models.CharField(max_length=11, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_password_reset_required = models.BooleanField(default=False)
    Organization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name if self.name else self.mobile

    def get_all_permissions(self):
        if self.role:
            return set(self.role.role_permissions.values_list(
                'permission__codename', flat=True))
        return set()

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_active=True, is_deleted=False)

    @classmethod
    def get_by_id(cls, user_id):
        try:
            return cls.objects.get(id=user_id, is_deleted=False)
        except cls.DoesNotExist:
            return None
