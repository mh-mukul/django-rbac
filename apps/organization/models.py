from django.db import models
from apps.core.models import AbstractBaseFields


class Organization(AbstractBaseFields):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "organizations"
