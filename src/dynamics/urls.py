from django.urls import re_path

from dynamics.views import DynamicsView

urlpatterns = [
    re_path(
        r"((?P<at>\d{4}-\d{2}-\d{2})/)?((?P<fuel>\d*)/)?((?P<currency>\d*)/)?",
        DynamicsView.as_view(),
        name="dynamics",
    )
]
