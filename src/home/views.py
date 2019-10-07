from typing import NamedTuple, Text, Tuple

from django.shortcuts import render


class PriceData(NamedTuple):
    value: float
    sign: Text


class FuelData(NamedTuple):
    color: Text
    prices: Tuple


def get_prices():
    return {
        "98": FuelData(
            color="#9500D0",
            prices=(
                PriceData(1.9, "byn"),
                PriceData(0.95, "usd"),
                PriceData(0.7, "eur"),
                PriceData(1900, "rub"),
            ),
        ),
        "95": FuelData(
            color="#E80000",
            prices=(
                PriceData(1.7, "byn"),
                PriceData(0.8, "usd"),
                PriceData(0.65, "eur"),
                PriceData(1700, "rub"),
            ),
        ),
        "92": FuelData(
            color="#C19B10",
            prices=(
                PriceData(1.5, "byn"),
                PriceData(0.75, "usd"),
                PriceData(0.6, "eur"),
                PriceData(1500, "rub"),
            ),
        ),
        "DT": FuelData(
            color="#00BE06",
            prices=(
                PriceData(1.8, "byn"),
                PriceData(0.9, "usd"),
                PriceData(0.78, "eur"),
                PriceData(1800, "rub"),
            ),
        ),
        "LPG": FuelData(
            color="#0088D0",
            prices=(
                PriceData(0.9, "byn"),
                PriceData(0.45, "usd"),
                PriceData(0.4, "eur"),
                PriceData(900, "rub"),
            ),
        ),
    }


def actual(request):
    return render(request, "home/index.html", {"prices": get_prices().items()})
