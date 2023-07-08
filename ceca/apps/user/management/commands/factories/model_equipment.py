import random

from factory.django import DjangoModelFactory
from faker import Faker

from apps.equipment.models import ModelEquipment, ModelType
from apps.vendor.models import Vendor

faker = Faker()


class ModelEquipmentFactory(DjangoModelFactory):
    class Meta:
        model = ModelEquipment
        django_get_or_create = ('name',)

    status = ModelEquipment.Status.ACTIVATED
    name = lambda: faker.bothify(text='????-####')
    vendor = lambda: random.choice(Vendor.objects.all())
    type = lambda: random.choice(ModelType.objects.all())
