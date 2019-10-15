from django.urls import path

from . import views

urlpatterns = [path("", views.ActualView.as_view(), name="actual")]
