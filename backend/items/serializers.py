import cloudinary
from django.contrib.auth import get_user_model
from rest_framework import serializers

from items.models import Item, ItemLog


class ItemLogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    image = serializers.ImageField(required=True, allow_null=False)

    class Meta:
        model = ItemLog
        fields = ["id", "item", "user", "image", "note", "created_at"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # instance.image が存在する場合、Cloudinary の URL に差し替える
        if instance.image:
            # Cloudinaryのリサイズ用URLを手動で組み立てる
            # instance.image.public_id は保存された画像のID（例: boot_logs/lvs4...）
            url = cloudinary.utils.cloudinary_url(
                instance.image.public_id,
                width=800,
                height=800,
                crop="limit",
                quality="auto",
                fetch_format="auto",
                secure=True,
            )[0]  # [0]にURLが入っています

            ret["image"] = url
        return ret


class ItemDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    logs = ItemLogSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "user",
            "brand",
            "model",
            "leather",
            "created_at",
            "logs",
        ]


class ItemListSerializer(serializers.ModelSerializer):
    items = ItemDetailSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "items"]


class ItemCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Item
        fields = ["user", "_type", "brand", "model", "leather"]
