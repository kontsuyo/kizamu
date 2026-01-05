from django.db import models

from config import settings


class BootItem(models.Model):
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
