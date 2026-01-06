from rest_framework import serializers

from items.models import BootItem


class BootItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BootItem
        fields = ["id", "user", "brand", "model", "leather", "created_at"]
