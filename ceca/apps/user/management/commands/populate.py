import datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from apps.equipment.models import ModelType
from apps.user.management.commands.factories.client_factory import ClientFactory
from apps.user.management.commands.factories.equipment import EquipmentFactory
from apps.user.management.commands.factories.model_equipment import ModelEquipmentFactory
from apps.user.management.commands.factories.model_type_factory import ModelTypeDefaultValues, ModelTypeFactory
from apps.user.management.commands.factories.vendor_factory import VendorFactory, VendorDefaultValues
from apps.user.models import CustomUser
from apps.vendor.models import Vendor


class Command(BaseCommand):
    help: str = "Add initial data into the database"

    def create_default_user(self) -> None:
        has_users: bool = CustomUser.objects.all().exists()
        if has_users:
            return

        CustomUser.objects.create_user(username="admin", email="admin@admin.com", password="admin",
                                       date_created=make_aware(datetime.datetime.now()))

    def create_vendors(self) -> None:
        data_already_exists: bool = Vendor.objects.filter(name=VendorDefaultValues.CISCO.name).exists()
        if data_already_exists:
            return

        VendorFactory.create_batch(len(VendorDefaultValues))

    def model_types(self) -> None:
        data_already_exists: bool = ModelType.objects.filter(name=ModelTypeDefaultValues.CORE.name).exists()
        if data_already_exists:
            return

        ModelTypeFactory.create_batch(len(ModelTypeDefaultValues))

    def model_equipment(self) -> None:
        ModelEquipmentFactory.create_batch(100)

    def create_clients(self) -> None:
        ClientFactory.create_batch(100)

    def create_equipments(self) -> None:
        EquipmentFactory.create_batch(2000)

    def handle(self, *args, **options) -> None:
        self.create_default_user()
        self.create_vendors()
        self.model_types()
        self.model_equipment()
        self.create_clients()
        self.create_equipments()
