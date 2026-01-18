import cloudinary
from django.contrib.auth import get_user_model
from rest_framework import serializers

from items.models import Item, Photo


class PhotoUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True, allow_null=False)
    user = serializers.ReadOnlyField(source="user.username")
    wore_on = serializers.DateField(format="%Y-%m-%d")  # pyright: ignore[reportArgumentType]

    class Meta:
        model = Photo
        fields = ["image", "item_id", "wore_on", "note", "user"]


class PhotoDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    image = serializers.ImageField(required=True, allow_null=False)

    class Meta:
        model = Photo
        fields = [
            "id",
            "item_id",
            "image",
            "wore_on",
            "note",
            "user",
        ]

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


class PhotoEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id", "wore_on", "note"]


class PhotoDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id"]


class ItemDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    photos = PhotoDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "brand",
            "model_name",
            "leather",
            "user",
            "created_at",
            "photos",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    items = ItemDetailSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "items"]


class ItemCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Item
        fields = ["user", "_type", "brand", "model_name", "leather"]
