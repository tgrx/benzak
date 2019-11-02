from django.db import models


class Currency(models.Model):
    name = models.TextField(unique=True)
    symbol = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "currency"
        ordering = ["name"]

    def __repr__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.name}"

    def __str__(self):
        return f"{self.name} ({self.symbol})"
