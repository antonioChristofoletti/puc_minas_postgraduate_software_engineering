import factory
from factory.django import DjangoModelFactory

from apps.client.models import Client


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client
        django_get_or_create = ('name',)

    status = Client.Status.ACTIVATED
    name = factory.Faker("company")
