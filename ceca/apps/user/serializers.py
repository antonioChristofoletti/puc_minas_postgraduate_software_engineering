from rest_framework import serializers

from apps.user.models import CustomUser


class CustomUserSeralizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email"]

    def create(validated_data):
        return CustomUser.objects.create(**validated_data)
