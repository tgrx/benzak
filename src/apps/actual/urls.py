from django.urls import path

from apps.actual.views import ActualView

urlpatterns = [path("", ActualView.as_view(), name="actual")]
