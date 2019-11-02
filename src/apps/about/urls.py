from django.urls import path

from apps.about.views import AboutView

urlpatterns = [path("", AboutView.as_view(), name="about")]
