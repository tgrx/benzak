import os
from datetime import date

from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase

from apps.api.models import ApiSettings
from apps.dynamics.models import Currency
from apps.dynamics.models import Fuel
from apps.dynamics.models import PriceHistory

User = get_user_model()


class ApiTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create_user(
            "testadmin", "testadmin@test.com", "testadminpassword"
        )
        self.admin.is_superuser = True
        self.admin.is_staff = True
        self.admin.save()
        self.admin_token = os.urandom(8).hex()

        api_settings = ApiSettings(user=self.admin, token=self.admin_token)
        api_settings.save()

        self.user = User.objects.create_user("test", "test@test.com", "testpassword")
        self.user_token = os.urandom(8).hex()

        api_settings = ApiSettings(user=self.user, token=self.user_token)
        api_settings.save()

    def create_currency(self, name) -> Currency:
        currency = Currency(name=name, symbol=name[0].upper())
        currency.save()

        return currency

    def create_fuel(self, name) -> Fuel:
        fuel = Fuel(name=f"AI-{name}", short_name=f"{name}", color=f"color-{name}")
        fuel.save()

        return fuel

    def create_price_history(
        self, at: date, currency: Currency, fuel: Fuel, value: int
    ) -> PriceHistory:
        ph = PriceHistory(at=at, currency=currency, fuel=fuel, price=value)
        ph.save()

        return ph
