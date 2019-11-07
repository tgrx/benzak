from rest_framework import status

from apps.api.tests.base import ApiTest


class FuelApiTest(ApiTest):
    def test_read(self):
        fuel95 = self.create_fuel("95")
        fuel98 = self.create_fuel("98")

        response = self.client.get("/api/v1/fuel/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertEqual(len(payload), 2)

        for obj, fuel in zip(payload, (fuel95, fuel98)):
            self.assertTrue(obj)
            self.assertIsInstance(obj, dict)

            self.assertDictEqual(
                obj,
                {
                    "id": fuel.pk,
                    "name": fuel.name,
                    "short_name": fuel.short_name,
                    "color": fuel.color,
                },
            )

    def test_retrieve(self):
        fuel95 = self.create_fuel("95")

        response = self.client.get(f"/api/v1/fuel/{fuel95.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertIsInstance(payload, dict)

        self.assertDictEqual(
            payload,
            {
                "id": fuel95.pk,
                "name": fuel95.name,
                "short_name": fuel95.short_name,
                "color": fuel95.color,
            },
        )

    def test_create(self):
        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {"name": "xxx"}

        response = self.client.post("/api/v1/fuel/", data=data, **user_headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.post("/api/v1/fuel/", data=data, **admin_headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update(self):
        fuel = self.create_fuel("99")

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {"name": "xxx"}

        response = self.client.put(
            f"/api/v1/fuel/{fuel.pk}/", data=data, **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(
            f"/api/v1/fuel/{fuel.pk}/", data=data, **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(
            f"/api/v1/fuel/{fuel.pk}/", data=data, **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(
            f"/api/v1/fuel/{fuel.pk}/", data=data, **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        fuel = self.create_fuel("99")

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {"name": "xxx"}

        response = self.client.delete(
            f"/api/v1/fuel/{fuel.pk}/", data=data, **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(
            f"/api/v1/fuel/{fuel.pk}/", data=data, **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
