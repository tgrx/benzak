from rest_framework import status

from apps.api.tests.base import ApiTest


class CurrencyApiTest(ApiTest):
    def test_read(self):
        byn = self.create_currency("byn")
        eur = self.create_currency("eur")

        response = self.client.get("/api/v1/currency/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertEqual(len(payload), 2)

        for obj, currency in zip(payload, (byn, eur)):
            self.assertTrue(obj)
            self.assertIsInstance(obj, dict)

            self.assertDictEqual(
                obj,
                {"id": currency.pk, "name": currency.name, "symbol": currency.symbol},
            )

    def test_retrieve(self):
        usd = self.create_currency("usd")

        response = self.client.get(f"/api/v1/currency/{usd.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertIsInstance(payload, dict)

        self.assertDictEqual(
            payload, {"id": usd.pk, "name": usd.name, "symbol": usd.symbol}
        )

    def test_create(self):
        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {"name": "xxx", "symbol": "x"}

        response = self.client.post("/api/v1/currency/", data=data, **user_headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.post("/api/v1/currency/", data=data, **admin_headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update(self):
        usd = self.create_currency("usd")

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {"name": "xxx", "symbol": "x"}

        response = self.client.put(
            f"/api/v1/currency/{usd.pk}/", data=data, **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(
            f"/api/v1/currency/{usd.pk}/", data=data, **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(
            f"/api/v1/currency/{usd.pk}/", data=data, **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(
            f"/api/v1/currency/{usd.pk}/", data=data, **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        rub = self.create_currency("rub")

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {"name": "xxx", "symbol": "x"}

        response = self.client.delete(
            f"/api/v1/currency/{rub.pk}/", data=data, **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(
            f"/api/v1/currency/{rub.pk}/", data=data, **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
