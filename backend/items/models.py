from cloudinary.models import CloudinaryField  # 追加
from django.db import models

from config import settings


class BootItem(models.Model):
    id: int
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="boot_items",
    )
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    leather = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.brand} {self.model}"


class BootLog(models.Model):
    id: int
    boot_item = models.ForeignKey(
        BootItem,
        on_delete=models.CASCADE,
        related_name="logs",
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = CloudinaryField(
        "image",
        folder="boot_logs/",
        blank=True,
        null=True,
    )
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Log for {self.boot_item} at {self.created_at}"
