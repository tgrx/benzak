from rest_framework import status

from apps.api.tests.base import ApiTest


class DynamicsAnonApiTest(ApiTest):
    def test_read(self):
        response = self.client.get("/api/v1/dynamics/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get("/api/v1/price-history/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create(self):
        response = self.client.post("/api/v1/dynamics/", data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        response = self.client.put("/api/v1/dynamics/1/", data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch("/api/v1/dynamics/", data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        response = self.client.delete("/api/v1/dynamics/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
