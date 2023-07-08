import datetime
import random

from django.utils.timezone import make_aware
from factory.django import DjangoModelFactory
from faker import Faker

from apps.equipment.models import Equipment, ModelEquipment
from apps.user.management.commands.factories.port_equipment import PortEquipmentFactory
from apps.user.models import CustomUser

faker = Faker()


class EquipmentFactory(DjangoModelFactory):
    class Meta:
        model = Equipment
        django_get_or_create = ('hostname',)

    status = Equipment.Status.ACTIVATED
    hostname = lambda: f"hostname_{EquipmentFactory.get_last_id()}"
    model = lambda: random.choice(ModelEquipment.objects.all())
    os_version = lambda: f"os_{EquipmentFactory.get_last_id()}"
    ip = lambda: faker.ipv4()
    observation = lambda: faker.paragraph(nb_sentences=2)
    created_by = lambda: random.choice(CustomUser.objects.all())
    date_created = lambda: make_aware(datetime.datetime.now())

    @classmethod
    def get_last_id(cls) -> int:
        if not Equipment.objects.last():
            return 0

        return Equipment.objects.last().id + 1

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        super()._create(model_class, *args, **kwargs)

        created_equipment = Equipment.objects.last()

        PortEquipmentFactory.create_batch(4, equipment=created_equipment)
