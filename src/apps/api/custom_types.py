from datetime import date
from decimal import Decimal
from typing import List
from typing import NamedTuple

from apps.dynamics.models import Currency
from apps.dynamics.models import Fuel


class DynPriceT(NamedTuple):
    currency: Currency
    value: Decimal


class DynFuelT(NamedTuple):
    fuel: Fuel
    prices: List[DynPriceT]


class DynT(NamedTuple):
    at: date
    fuels: List[DynFuelT]
