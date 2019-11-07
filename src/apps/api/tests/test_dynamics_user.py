from datetime import date

from rest_framework import status

from apps.api.tests.base import ApiTest


class DynamicsUserApiTest(ApiTest):
    def test_read(self):
        usd = self.create_currency("usd")
        eur = self.create_currency("eur")
        ai95 = self.create_fuel("95")
        at = date(year=2019, month=1, day=13)
        self.create_price_history(at=at, currency=eur, fuel=ai95, value=321)
        self.create_price_history(at=at, currency=usd, fuel=ai95, value=123)

        headers = {"HTTP_AUTHORIZATION": self.user_token}

        response = self.client.get(f"/api/v1/dynamics/", **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertIsInstance(payload, list)
        self.assertEqual(len(payload), 1)

        record = payload[0]
        self.assertIsInstance(record, dict)
        self.assertEqual(record["at"], at.strftime("%Y-%m-%d"))
        self.assertIn("fuels", record)

        fuels = record["fuels"]
        self.assertIsInstance(fuels, list)
        self.assertEqual(len(fuels), 1)

        fuel = fuels[0]
        self.assertIsInstance(fuel, dict)
        self.assertEqual(fuel["fuel"]["name"], ai95.name)
        self.assertIn("prices", fuel)

        prices = fuel["prices"]
        self.assertIsInstance(prices, list)
        self.assertEqual(len(prices), 2)

        for price, (currency, value) in zip(prices, ((eur, 321), (usd, 123))):
            self.assertEqual(price["currency"]["name"], currency.name)
            self.assertEqual(price["currency"]["symbol"], currency.symbol)
            self.assertEqual(int(float(price["value"])), value)

    def test_create(self):
        headers = {"HTTP_AUTHORIZATION": self.user_token}

        response = self.client.post("/api/v1/dynamics/", data={}, **headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update(self):
        headers = {"HTTP_AUTHORIZATION": self.user_token}

        response = self.client.put("/api/v1/dynamics/1/", data={}, **headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch("/api/v1/dynamics/1/", data={}, **headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        headers = {"HTTP_AUTHORIZATION": self.user_token}

        response = self.client.delete("/api/v1/dynamics/1/", **headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
