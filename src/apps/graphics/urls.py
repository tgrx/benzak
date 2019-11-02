from django.urls import path

from apps.graphics.views import GraphicsView

urlpatterns = [path("", GraphicsView.as_view(), name="graphics")]
