from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("home.urls")),
    path("about/", include("about.urls")),
    path("admin/", admin.site.urls),
    path("dynamics/", include("dynamics.urls")),
    path("graphics/", include("graphics.urls")),
]
