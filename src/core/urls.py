from django.contrib import admin
from django.urls import path, include

urlpatterns = [path("about/", include("about.urls")), path("admin/", admin.site.urls)]
