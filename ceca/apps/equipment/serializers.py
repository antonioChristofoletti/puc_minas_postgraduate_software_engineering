from rest_framework import serializers

from apps.equipment.models import ModelEquipment, Equipment
from apps.user.serializers import CustomUserSeralizer
from apps.vendor.serializers import VendorSerializer


class ModelEquipmentSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)

    class Meta:
        model = ModelEquipment
        fields = "__all__"
        depth = 1

    def create(validated_data):
        return ModelEquipment.objects.create(**validated_data)


class EquipmentSerializer(serializers.ModelSerializer):
    model = ModelEquipmentSerializer(read_only=True)
    updated_by = CustomUserSeralizer(read_only=True)
    created_by = CustomUserSeralizer(read_only=True)

    class Meta:
        model = Equipment
        fields = "__all__"
        depth = 1

    def create(validated_data):
        return Equipment.objects.create(**validated_data)