from rest_framework import serializers

from accounts.models import CustomUser
from items.models import Item


class CustomUserSerializer(serializers.ModelSerializer):
    boot_items = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Item.objects.all()
    )

    class Meta:
        model = CustomUser
        fields = [
            "url",
            "id",
            "username",
            "boot_items",
        ]
