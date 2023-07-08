from datetime import datetime

from django.db import models

from apps.equipment.models import Equipment
from apps.user.models import CustomUser


class InfoExtracted(models.Model):
    class Meta:
        db_table = "info_extracted"

    command = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(null=False, blank=False)

    equipment = models.ForeignKey(
        to=Equipment,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="info_extracted_list"
    )

    created_by = models.ForeignKey(
        to=CustomUser,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="info_extracted_list"
    )

    date_created = models.DateTimeField(null=False, blank=False, default=datetime.now)

