from rest_framework import serializers

from items.models import BootItem


class BootItemSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = BootItem
        fields = [
            "url",
            "id",
            "user",
            "brand",
            "model",
            "leather",
            "created_at",
        ]
