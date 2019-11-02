from django.views.generic import ListView

from apps.dynamics.models import Currency, Fuel, PriceHistory


class ActualView(ListView):
    template_name = "actual/index.html"

    def get_queryset(self):
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
