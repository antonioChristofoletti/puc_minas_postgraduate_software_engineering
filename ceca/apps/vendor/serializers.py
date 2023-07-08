from rest_framework import serializers

from apps.vendor.models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"

    def create(validated_data):
        return Vendor.objects.create(**validated_data)