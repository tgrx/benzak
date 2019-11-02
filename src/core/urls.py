from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("home.urls")),
    path("about/", include("about.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("dynamics/", include("dynamics.urls")),
    path("graphics/", include("graphics.urls")),
    path("o/", include("onboarding.urls")),
]
