from datetime import date, datetime
from typing import Dict

from django.db import IntegrityError, transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from apps.api.custom_types import DynFuelT, DynPriceT, DynT
from apps.api.impl.auth import CustomTokenAuthentication
from apps.api.impl.v1.serializers import (
    CurrencySerializer,
    DynamicsSerializer,
    FuelSerializer,
    PriceHistorySerializer,
)
from apps.dynamics.models import Currency, Fuel, PriceHistory


class CurrencyViewSet(ReadOnlyModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class FuelViewSet(ReadOnlyModelViewSet):
    queryset = Fuel.objects.all()
    serializer_class = FuelSerializer


class PriceHistoryViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet
):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = PriceHistory.objects.all()
    serializer_class = PriceHistorySerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as err:
            return JsonResponse(
                data={"error": str(err)}, status=status.HTTP_400_BAD_REQUEST
            )


class DynamicsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DynamicsSerializer
    lookup_field = "at"

    def get_queryset(self):
        qs = self.get_grouped()

        return sorted(qs.values(), key=lambda _i: _i.at, reverse=True)

    def get_object(self):
        qs = self.get_queryset()
        if qs:
            return qs[0]
        return None

    def get_grouped(self) -> Dict[date, DynT]:
        queryset = PriceHistory.objects.all()

        if self.detail:
            at_raw = self.kwargs[self.lookup_field]
            at = datetime.strptime(at_raw, "%Y-%m-%d").date()
            queryset = queryset.filter(at=at)

        raw = {}

        for item in queryset:
            dyns = raw.setdefault(item.at, {})
            fuels = dyns.setdefault(item.fuel, {})
            fuels[item.currency] = item.price

        result = {}

        for at, fuels in raw.items():
            dyn = DynT(at=at, fuels=[])

            for fuel, prices in fuels.items():
                d_fuel = DynFuelT(fuel=fuel, prices=[])
                for currency, price in prices.items():
                    d_price = DynPriceT(currency=currency, value=price)
                    d_fuel.prices.append(d_price)
                d_fuel.prices.sort(key=lambda _i: _i.currency.name)
                dyn.fuels.append(d_fuel)

            dyn.fuels.sort(key=lambda _i: _i.fuel.name)
            result[at] = dyn

        return dict(result)
