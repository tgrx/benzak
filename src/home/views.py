from typing import NamedTuple

from django.shortcuts import render


class FuelData(NamedTuple):
    color: str
    price: float


def get_prices():
    return {
        "98": FuelData("#9500D0", 1.9),
        "95": FuelData("#E80000", 1.7),
        "92": FuelData("#C19B10", 1.5),
        "DT": FuelData("#00BE06", 1.8),
        "LPG": FuelData("#0088D0", 0.9),
    }


def index(request):
    return render(request, "index.html", {"prices": get_prices().items()})
