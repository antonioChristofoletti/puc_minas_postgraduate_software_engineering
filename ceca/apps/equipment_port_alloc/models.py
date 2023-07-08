from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.client.models import Client
from apps.equipment.models import PortEquipment
from apps.user.models import CustomUser


class EquipmentPortAlloc(models.Model):
    class Meta:
        db_table = "equipment_port_alloc"

    class EquipmentPortAllocStatus(models.TextChoices):
        ACTIVATED = 'A', _('Activated')
        DISABLE = 'D', _('Disabled')

    status = models.CharField(max_length=100, choices=EquipmentPortAllocStatus.choices, default=EquipmentPortAllocStatus.ACTIVATED)

    client = models.ForeignKey(
        to=Client,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="equipments_port_allocs"
    )

    port = models.ForeignKey(
        to=PortEquipment,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="port_alloc_list"
    )

    title = models.CharField(max_length=100, null=False, blank=False)

    date_start = models.DateTimeField(null=False, blank=False)
    date_end = models.DateTimeField(null=False, blank=False)

    observation = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(
        to=CustomUser,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="created_equipments_port_allocs"
    )

    updated_by = models.ForeignKey(
        to=CustomUser,
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name="updated_equipments_port_allocs"
    )

    date_created = models.DateTimeField(null=False, blank=False, default=datetime.now)
    date_updated = models.DateTimeField(null=True, blank=False, default=None)


