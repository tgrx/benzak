from django.urls import path

from . import views

urlpatterns = [path("", views.actual, name="actual")]
