from datetime import date

from rest_framework import status

from apps.api.tests.base import ApiTest
from apps.dynamics.models import PriceHistory


class PriceHistoryAdminApiTest(ApiTest):
    def test_read(self):
        usd = self.create_currency("usd")
        ai95 = self.create_fuel("95")
        at1 = date(year=2019, month=1, day=13)
        at2 = date(year=2019, month=1, day=14)
        ph1 = self.create_price_history(at=at1, currency=usd, fuel=ai95, value=100)
        ph2 = self.create_price_history(at=at2, currency=usd, fuel=ai95, value=200)

        headers = {"HTTP_AUTHORIZATION": self.admin_token}

        response = self.client.get(f"/api/v1/price-history/", **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertIsInstance(payload, list)
        self.assertEqual(len(payload), 2)

        for obj, ph in zip(payload, (ph2, ph1)):
            self.assertTrue(obj)
            self.assertIsInstance(obj, dict)

            self.assertDictEqual(
                obj,
                {
                    "id": ph.pk,
                    "currency": usd.pk,
                    "fuel": ai95.pk,
                    "at": ph.at.strftime("%Y-%m-%d"),
                    "price": f"{ph.price:.4f}",
                },
            )

        for ph in (ph1, ph2):
            response = self.client.get(f"/api/v1/price-history/{ph.pk}/", **headers)
            payload = response.json()
            self.assertIsInstance(payload, dict)
            self.assertDictEqual(
                payload,
                {
                    "id": ph.pk,
                    "currency": usd.pk,
                    "fuel": ai95.pk,
                    "at": ph.at.strftime("%Y-%m-%d"),
                    "price": f"{ph.price:.4f}",
                },
            )

    def test_create(self):
        usd = self.create_currency("usd")
        ai95 = self.create_fuel("95")
        at = date(year=2019, month=1, day=13)

        headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {
            "price": 1488,
            "currency": usd.pk,
            "fuel": ai95.pk,
            "at": at.strftime("%Y-%m-%d"),
        }

        response = self.client.post("/api/v1/price-history/", data=data, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload = response.json()
        self.assertIsInstance(payload, dict)
        self.assertIn("id", payload)

        new_id = payload["id"]
        self.assertTrue(new_id)

        ph = PriceHistory.objects.filter(pk=new_id)
        self.assertEqual(len(ph), 1)
        ph = ph[0]

        self.assertEqual(ph.at, at)
        self.assertEqual(ph.currency, usd)
        self.assertEqual(ph.fuel, ai95)
        self.assertEqual(ph.price, 1488)

        # check singular price

        data_dup = {
            "price": 8814,
            "currency": usd.pk,
            "fuel": ai95.pk,
            "at": at.strftime("%Y-%m-%d"),
        }

        response = self.client.post("/api/v1/price-history/", data=data_dup, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        phs = PriceHistory.objects.all()
        self.assertEqual(len(phs), 1)

    def test_replace(self):
        usd = self.create_currency("usd")
        ai95 = self.create_fuel("95")
        at = date(year=2019, month=1, day=13)

        ph = self.create_price_history(at, usd, ai95, 1)

        headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {
            "price": 1488,
            "currency": usd.pk,
            "fuel": ai95.pk,
            "at": at.strftime("%Y-%m-%d"),
        }

        response = self.client.put(
            f"/api/v1/price-history/{ph.pk}/",
            data=data,
            content_type="application/json",
            **headers,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update(self):
        usd = self.create_currency("usd")
        ai95 = self.create_fuel("95")
        at = date(year=2019, month=1, day=13)

        ph = self.create_price_history(at, usd, ai95, 1)

        headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {"price": 1488}

        response = self.client.patch(
            f"/api/v1/price-history/{ph.pk}/",
            data=data,
            content_type="application/json",
            **headers,
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
