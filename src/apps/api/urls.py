from django.urls import path

from apps.api.views import ApiResetTokenView, ApiSettingsView

urlpatterns = [
    path("settings/", ApiSettingsView.as_view(), name="api_settings"),
    path("settings/reset-token/", ApiResetTokenView.as_view(), name="api_reset_token"),
]
