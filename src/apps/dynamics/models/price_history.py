from django.db import models

from apps.dynamics.models import Currency
from apps.dynamics.models import Fuel


class PriceHistory(models.Model):
    price = models.DecimalField(max_digits=24, decimal_places=4)
    at = models.DateField()

    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    fuel = models.ForeignKey(Fuel, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "price history"
        ordering = ["-at", "fuel", "currency"]
        constraints = [
            models.UniqueConstraint(
                fields=["at", "fuel", "currency"], name="singular_price"
            )
        ]

    def __repr__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.currency} / {self.fuel}"

    def __str__(self):
        return f"Price {self.price} {self.currency} of {self.fuel} @ {self.at}"
