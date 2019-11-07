from datetime import date

from rest_framework import status

from apps.api.tests.base import ApiTest


class PriceHistoryUserApiTest(ApiTest):
    def test_read(self):
        usd = self.create_currency("usd")
        ai95 = self.create_fuel("95")
        at = date(year=2019, month=1, day=13)
        ph = self.create_price_history(at=at, currency=usd, fuel=ai95, value=123)

        headers = {"HTTP_AUTHORIZATION": self.user_token}

        response = self.client.get(f"/api/v1/price-history/", **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(f"/api/v1/price-history/{ph.pk}/", **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create(self):
        headers = {"HTTP_AUTHORIZATION": self.user_token}
        data = {"price": 1488}

        response = self.client.post("/api/v1/price-history/", data=data, **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        usd = self.create_currency("usd")
        ai95 = self.create_fuel("95")
        at = date(year=2019, month=1, day=13)
        ph = self.create_price_history(at=at, currency=usd, fuel=ai95, value=123)

        headers = {"HTTP_AUTHORIZATION": self.user_token}
        data = {"price": 1488}

        response = self.client.put(
            f"/api/v1/price-history/{ph.pk}/", data=data, **headers
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch(
            f"/api/v1/price-history/{ph.pk}/", data=data, **headers
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        usd = self.create_currency("usd")
        ai95 = self.create_fuel("95")
        at = date(year=2019, month=1, day=13)
        ph = self.create_price_history(at=at, currency=usd, fuel=ai95, value=123)

        headers = {"HTTP_AUTHORIZATION": self.user_token}

        response = self.client.delete(f"/api/v1/price-history/{ph.pk}/", **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
