from collections import namedtuple
from unittest.mock import patch

from rest_framework import status

from apps.api.tests.base import ApiTest


class TelegramApiTest(ApiTest):
    url = "/api/v1/telegram/"

    @patch("apps.api.impl.v1.views.TelegramView.bot_respond")
    def test_post(self, meth_bot_respond):
        meth_bot_respond.return_value = namedtuple("_", ["status_code"])(200)
        message = {
            "message": {
                "chat": {"id": "chat_id"},
                "from": {"id": "from_id", "first_name": "from_first_name"},
                "id": "message_id",
                "text": "text",
            }
        }

        response = self.client.post(
            self.url, data=message, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        meth_bot_respond.assert_called_once()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
