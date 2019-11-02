from django.db import models


class Fuel(models.Model):
    name = models.TextField(unique=True)
    short_name = models.TextField(unique=True)
    color = models.TextField(unique=True)

    class Meta:
        verbose_name_plural = "fuels"
        ordering = ["name"]

    def __repr__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.name}"

    def __str__(self):
        return f"{self.name} ({self.pk})"
