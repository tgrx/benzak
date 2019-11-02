from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ApiSettings(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="api_settings"
    )
    token = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "API settings"
        ordering = ["user"]

    def __repr__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.user}"

    def __str__(self):
        return repr(self)
