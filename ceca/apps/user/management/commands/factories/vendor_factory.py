import enum

from factory.django import DjangoModelFactory
from faker import Faker

from apps.vendor.models import Vendor


class VendorDefaultValues(enum.Enum):
    NOKIA = "Nokia",
    CISCO = "Cisco",
    HUAWEI = "Huawei",
    JUNIPER = "Juniper"


faker = Faker()


class VendorFactory(DjangoModelFactory):
    class Meta:
        model = Vendor
        django_get_or_create = ('name',)

    status = Vendor.Status.ACTIVATED
    name = lambda: list(VendorDefaultValues)[faker.unique.random_int(min=0, max=len(VendorDefaultValues)-1)].name
