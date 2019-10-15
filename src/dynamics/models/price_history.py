from django.db import models as m

from dynamics.models import Currency, Fuel


class PriceHistory(m.Model):
    price = m.DecimalField(max_digits=24, decimal_places=4)
    at = m.DateField()

    currency = m.ForeignKey(Currency, on_delete=m.PROTECT)
    fuel = m.ForeignKey(Fuel, on_delete=m.PROTECT)

    class Meta:
        verbose_name_plural = "Price History"
        ordering = ["-at", "fuel", "currency"]

    def __repr__(self):
        return f"{self.__class__.__name__} #{self.pk}: {self.currency} / {self.fuel}"

    def __str__(self):
        return f"Price {self.price} {self.currency} of {self.fuel} @ {self.at}"
