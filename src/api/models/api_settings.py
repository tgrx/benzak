from django.contrib.auth import get_user_model
from django.db import models as m

User = get_user_model()


class ApiSettings(m.Model):
    user = m.OneToOneField(User, on_delete=m.CASCADE, related_name="api_settings")
    token = m.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "API settings"
        ordering = ["user"]

    def __repr__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.user}"

    def __str__(self):
        return repr(self)
