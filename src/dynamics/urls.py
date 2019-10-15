from django.urls import path

from dynamics.views import DynamicsView

urlpatterns = [path("", DynamicsView.as_view(), name="dynamics")]
