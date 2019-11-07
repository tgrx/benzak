from django.urls import include, path

urlpatterns = [path("v1/", include("apps.api.impl.v1.urls"))]
