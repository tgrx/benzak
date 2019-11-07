from django.urls import include, path

from apps.api.views import ApiResetTokenView, ApiSettingsView

urlpatterns = [
    path("", include("apps.api.impl.urls")),
    path("settings/", ApiSettingsView.as_view(), name="api_settings"),
    path("settings/reset-token/", ApiResetTokenView.as_view(), name="api_reset_token"),
]
