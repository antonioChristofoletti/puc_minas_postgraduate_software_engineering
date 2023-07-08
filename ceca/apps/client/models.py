from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    class Meta:
        db_table = "client"

    class Status(models.TextChoices):
        ACTIVATED = 'A', _('Activated')
        DISABLE = 'D', _('Disabled')

    status = models.CharField(max_length=100, choices=Status.choices, default=Status.ACTIVATED)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
