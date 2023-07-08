from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _


class TypeUser(models.Model):
    class Meta:
        db_table = "type_user"

    class TypeUserStatus(models.TextChoices):
        ACTIVATED = 'A', _('Activated')
        DISABLE = 'D', _('Disabled')

    status = models.CharField(max_length=100, choices=TypeUserStatus.choices, default=TypeUserStatus.ACTIVATED)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)


class RoleUser(models.Model):
    class Meta:
        db_table = "role_user"

    class TypeUserStatus(models.TextChoices):
        ACTIVATED = 'A', _('Activated')
        DISABLE = 'D', _('Disabled')

    status = models.CharField(max_length=100, choices=TypeUserStatus.choices, default=TypeUserStatus.ACTIVATED)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.CharField(max_length=100, null=False, blank=False)


class CustomUser(AbstractUser):
    class Meta:
        db_table = "user"

    email = models.EmailField(_('email address'), unique=True)

    type = models.ForeignKey(
        to=TypeUser,
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name='users'
    )

    roles = models.ManyToManyField(RoleUser, db_table="user_to_role", related_name="users")

    observation = models.TextField(null=True, blank=True)

    qtdy_auth_attempt = models.IntegerField(null=False, default=0)

    date_created = models.DateTimeField(null=False, blank=False, default=datetime.now)

    date_updated = models.DateTimeField(null=True, blank=False, default=None)

    created_by = models.ForeignKey(
        to="self",
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name="created_users"
    )

    updated_by = models.ForeignKey(
        to="self",
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name="updated_users"
    )
