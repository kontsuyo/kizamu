import cloudinary
from django.contrib.auth import get_user_model
from rest_framework import serializers

from items.models import Item, Photo


class ItemSummarySerializer(serializers.ModelSerializer):
    """Item詳細情報用の詳細情報用の軽量シリアライザー"""

    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Item
        fields = [
            "id",
            "brand",
            "model_name",
            "leather",
            "user",
            "created_at",
        ]


class PhotoUploadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True, allow_null=False)
    user = serializers.ReadOnlyField(source="user.username")
    wore_on = serializers.DateField(format="%Y-%m-%d")  # pyright: ignore[reportArgumentType]

    class Meta:
        model = Photo
        fields = ["image", "item", "wore_on", "note", "shared_feed", "user"]


class PhotoDetailSerializer(serializers.ModelSerializer):
    item = ItemSummarySerializer(read_only=True)
    image = serializers.ImageField(read_only=True)
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Photo
        fields = [
            "id",
            "item",
            "image",
            "wore_on",
            "note",
            "shared_feed",
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


class FeedSerializer(serializers.ModelSerializer):
    """フィード表示用シリアライザー"""

    user = serializers.ReadOnlyField(source="user.username")
    brand = serializers.ReadOnlyField(source="item.brand")
    model_name = serializers.ReadOnlyField(source="item.model_name")
    leather = serializers.ReadOnlyField(source="item.leather")
    image = serializers.SerializerMethodField()
    item_id = serializers.ReadOnlyField(source="item.id")

    class Meta:
        model = Photo
        fields = [
            "id",
            "item_id",
            "brand",
            "model_name",
            "leather",
            "image",
            "note",
            "shared_feed",
            "user",
            "created_at",
        ]

    def get_image(self, obj):
        # Cloudinaryのリサイズ済みURL
        if obj.image:
            url = cloudinary.utils.cloudinary_url(
                obj.image.public_id,
                width=400,
                height=400,
                crop="limit",
                quality="auto",
                fetch_format="auto",
                secure=True,
            )[0]
            return url
        return None
