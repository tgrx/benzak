from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api.impl.v1.views import (
    CurrencyViewSet,
    DynamicsViewSet,
    FuelViewSet,
    PriceHistoryViewSet,
)

router = DefaultRouter()
router.register("currency", CurrencyViewSet)
router.register("dynamics", DynamicsViewSet, "Dynamics")
router.register("fuel", FuelViewSet)
router.register("price-history", PriceHistoryViewSet)

urlpatterns = [path("", include(router.urls))]
