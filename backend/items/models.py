from cloudinary.models import CloudinaryField  # 追加
from django.db import models
from django.utils import timezone

from config import settings


class Item(models.Model):
    id: int
    Type = models.TextChoices("ItemType", "Footwear")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="items",
    )
    _type = models.CharField(choices=Type.choices, max_length=10)
    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    leather = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.brand} {self.model_name}"


class Photo(models.Model):
    id: int
    item_id = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = CloudinaryField(
        "image",
        folder="item_logs/",
        blank=False,
        null=False,
    )
    note = models.TextField(blank=True)
    wore_on = models.DateField(blank=False, null=False, default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-wore_on"]

    def __str__(self):
        return f"Log for {self.item_id} at {self.created_at}"
