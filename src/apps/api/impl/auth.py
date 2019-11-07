from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from apps.api.models import ApiSettings

User = get_user_model()


class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = self._get_token(request)
        if not token:
            return None

        try:
            api_settings = ApiSettings.objects.get(token=token)
            user = api_settings.user
            return user, None
        except ApiSettings.DoesNotExist:
            raise AuthenticationFailed(f"invalid token")

    def _get_token(self, request: Request):
        return request.META.get("HTTP_AUTHORIZATION")
