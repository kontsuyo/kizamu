from rest_framework import serializers

from items.models import BootItem, BootLog


class BootLogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = BootLog
        fields = ["id", "boot_item", "user", "note", "created_at"]


class BootItemSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    logs = BootLogSerializer(many=True, read_only=True)

    class Meta:
        model = BootItem
        fields = ["id", "user", "brand", "model", "leather", "created_at", "logs"]
