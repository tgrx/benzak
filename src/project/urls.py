from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("apps.actual.urls")),
    path("about/", include("apps.about.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("apps.api.urls")),
    path("dynamics/", include("apps.dynamics.urls")),
    path("graphics/", include("apps.graphics.urls")),
    path("o/", include("apps.onboarding.urls")),
]
