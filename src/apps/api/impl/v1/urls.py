from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.api.impl.v1.views import CurrencyViewSet
from apps.api.impl.v1.views import DynamicsViewSet
from apps.api.impl.v1.views import FuelViewSet
from apps.api.impl.v1.views import PriceHistoryViewSet
from apps.api.impl.v1.views import TelegramView

router = DefaultRouter()
router.register("currency", CurrencyViewSet)
router.register("dynamics", DynamicsViewSet, "Dynamics")
router.register("fuel", FuelViewSet)
router.register("price-history", PriceHistoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("telegram/", TelegramView.as_view()),
]
