from django.db import models as m


class Currency(m.Model):
    name = m.TextField(unique=True)
    symbol = m.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "currency"
        ordering = ["name"]

    def __repr__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.name}"

    def __str__(self):
        return f"{self.name} ({self.symbol})"
