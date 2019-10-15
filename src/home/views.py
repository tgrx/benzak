from typing import NamedTuple, Text, Tuple

from django.views.generic import TemplateView

from dynamics.models import Fuel, PriceHistory, Currency


class PriceData(NamedTuple):
    value: float
    sign: Text


class FuelData(NamedTuple):
    color: Text
    prices: Tuple


class ActualView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["actual"] = self.get_actual_prices()
        return context

    @staticmethod
    def get_actual_prices():
        fuels = Fuel.objects.all()
        currency = Currency.objects.all()

        prices = list(
            filter(
                lambda _v: _v[-1],
                (
                    (
                        f,
                        tuple(
                            filter(
                                bool,
                                (
                                    PriceHistory.objects.filter(fuel=f, currency=c)
                                    .order_by("-at")
                                    .first()
                                    for c in currency
                                ),
                            )
                        ),
                    )
                    for f in fuels
                ),
            )
        )

        return prices
