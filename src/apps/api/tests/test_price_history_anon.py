from datetime import date

from rest_framework import status

from apps.api.tests.base import ApiTest


class PriceHistoryAnonApiTest(ApiTest):
    def test_read(self):
        usd = self.create_currency("usd")
        ai95 = self.create_fuel("95")
        at = date(year=2019, month=1, day=13)
        ph = self.create_price_history(at=at, currency=usd, fuel=ai95, value=123)

        response = self.client.get(f"/api/v1/price-history/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(f"/api/v1/price-history/{ph.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create(self):
        data = {"price": 1488}

        response = self.client.post("/api/v1/price-history/", data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        usd = self.create_currency("usd")
        ai95 = self.create_fuel("95")
        at = date(year=2019, month=1, day=13)
        ph = self.create_price_history(at=at, currency=usd, fuel=ai95, value=123)

        data = {"price": 1488}

        response = self.client.put(f"/api/v1/price-history/{ph.pk}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch(f"/api/v1/price-history/{ph.pk}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        usd = self.create_currency("usd")
        ai95 = self.create_fuel("95")
        at = date(year=2019, month=1, day=13)
        ph = self.create_price_history(at=at, currency=usd, fuel=ai95, value=123)

        response = self.client.delete(f"/api/v1/price-history/{ph.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
