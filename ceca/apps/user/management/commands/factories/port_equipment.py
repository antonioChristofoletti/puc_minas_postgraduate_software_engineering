from factory.django import DjangoModelFactory
from faker import Faker

from apps.equipment.models import Equipment, PortEquipment

faker = Faker()


class PortEquipmentFactory(DjangoModelFactory):
    class Meta:
        model = PortEquipment
        django_get_or_create = ('port',)

    status = Equipment.Status.ACTIVATED
    observation = lambda: faker.paragraph(nb_sentences=2)
    port = lambda: faker.numerify(text='%/%/%')
