from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.models import CustomUser
from apps.vendor.models import Vendor


class ModelType(models.Model):
    objects = models.Manager()

    class Meta:
        db_table = "model_type"

    class Status(models.TextChoices):
        ACTIVATED = 'A', _('Activated')
        DISABLE = 'D', _('Disabled')

    status = models.CharField(max_length=100, choices=Status.choices, default=Status.ACTIVATED)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)


class ModelEquipment(models.Model):
    objects = models.Manager()

    class Meta:
        db_table = "model_equipment"

    class Status(models.TextChoices):
        ACTIVATED = 'A', _('Activated')
        DISABLE = 'D', _('Disabled')

    status = models.CharField(max_length=100, choices=Status.choices,
                              default=Status.ACTIVATED)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    vendor = models.ForeignKey(
        to=Vendor,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='model_equipments'
    )

    type = models.ForeignKey(
        to=ModelType,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='model_equipments'
    )

    def __str__(self):
        return self.name


class Equipment(models.Model):
    objects = models.Manager()

    class Meta:
        db_table = "equipment"

    class Status(models.TextChoices):
        ACTIVATED = 'A', _('Activated')
        DISABLE = 'D', _('Disabled')

    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.ACTIVATED)
    hostname = models.CharField(max_length=100, null=False, blank=False, unique=False)
    os_version = models.CharField(max_length=100, null=False, blank=False)
    ip = models.CharField(max_length=100, null=False, blank=False, unique=False)
    observation = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(null=False, blank=False, default=datetime.now)
    date_updated = models.DateTimeField(null=True, blank=False, default=None)

    created_by = models.ForeignKey(
        to=CustomUser,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="created_equipments"
    )

    updated_by = models.ForeignKey(
        to=CustomUser,
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name="updated_equipments"
    )

    model = models.ForeignKey(
        to=ModelEquipment,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='equipments'
    )


class PortEquipment(models.Model):
    objects = models.Manager()

    class Meta:
        db_table = "port_equipment"

    class PortEquipmentStatus(models.TextChoices):
        ACTIVATED = 'A', _('Activated')
        DISABLE = 'D', _('Disabled')

    status = models.CharField(max_length=100, choices=PortEquipmentStatus.choices,
                              default=PortEquipmentStatus.ACTIVATED)
    port = models.CharField(max_length=100, null=False, blank=False)
    observation = models.TextField(null=True, blank=True)

    equipment = models.ForeignKey(
        to=Equipment,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='ports'
    )
