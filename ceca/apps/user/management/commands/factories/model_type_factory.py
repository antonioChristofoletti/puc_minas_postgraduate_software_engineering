import enum

from factory.django import DjangoModelFactory
from faker import Faker

from apps.equipment.models import ModelType
from apps.vendor.models import Vendor


class ModelTypeDefaultValues(enum.Enum):
    DISTRIBUTION = "Distribution",
    CORE = "Core",
    ACCESS = "Access"


faker = Faker()


class ModelTypeFactory(DjangoModelFactory):
    class Meta:
        model = ModelType
        django_get_or_create = ('name',)

    status = Vendor.Status.ACTIVATED
    name = lambda: list(ModelTypeDefaultValues)[faker.unique.random_int(min=0, max=len(ModelTypeDefaultValues)-1)].name
