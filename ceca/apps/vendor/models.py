from django.db import models
from django.utils.translation import gettext_lazy as _


class Vendor(models.Model):
    objects = models.Manager()

    class Meta:
        db_table = "vendor"

    class Status(models.TextChoices):
        ACTIVATED = 'A', _('Activated')
        DISABLE = 'D', _('Disabled')

    status = models.CharField(max_length=100, choices=Status.choices, default=Status.ACTIVATED)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
