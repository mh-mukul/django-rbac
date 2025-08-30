from django.db import models
from django.conf import settings
from django.utils import timezone


class AbstractModelManager(models.Manager):
    def get_dataset(self):
        return self.filter(is_deleted=False).order_by('-created_at')


class AbstractBaseFields(models.Model):
    is_active = models.BooleanField(
        ('Is Active'), default=True
    )
    is_deleted = models.BooleanField(
        ('Is Deleted'), default=False
    )
    created_at = models.DateTimeField(
        ('Created At'), auto_now_add=True, null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="%(app_label)s_%(class)s_createdby"
    )
    updated_at = models.DateTimeField(
        ('Last Updated'), auto_now=True, null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="%(app_label)s_%(class)s_updated"
    )

    objects = AbstractModelManager()

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

    def soft_deactive(self):
        self.is_active = False
        self.save()

    def soft_active(self):
        self.is_active = True
        self.save()

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_active=True, is_deleted=False)

    @classmethod
    def get_all(cls):
        return cls.objects.filter(is_deleted=False)

    @classmethod
    def get_by_id(cls, pk, organization=None):
        try:
            if organization:
                return cls.objects.get(pk=pk, is_deleted=False, organization=organization)
            return cls.objects.get(pk=pk, is_deleted=False)
        except cls.DoesNotExist:
            return None
