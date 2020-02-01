from datetime import date
from datetime import datetime
from typing import Dict

import requests
from django.db import IntegrityError
from django.db import transaction
from django.http import JsonResponse
from dynaconf import settings
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.api.custom_types import DynFuelT
from apps.api.custom_types import DynPriceT
from apps.api.custom_types import DynT
from apps.api.impl.auth import CustomTokenAuthentication
from apps.api.impl.v1.serializers import CurrencySerializer
from apps.api.impl.v1.serializers import DynamicsSerializer
from apps.api.impl.v1.serializers import FuelSerializer
from apps.api.impl.v1.serializers import PriceHistorySerializer
from apps.dynamics.models import Currency
from apps.dynamics.models import Fuel
from apps.dynamics.models import PriceHistory


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


class TelegramView(APIView):
    def bot_respond(self, chat, message, bot_response):
        bot_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BENZAKBOT_TOKEN}/sendMessage"
        tg_resp = requests.post(
            bot_url,
            json={
                "chat_id": chat["id"],
                "parse_mode": "Markdown",
                "reply_to_message_id": message["message_id"],
                "text": bot_response,
            },
        )

        return tg_resp

    def post(self, request: Request, *_args, **_kw):
        if not settings.TELEGRAM_BENZAKBOT_TOKEN or not request:
            raise PermissionDenied("unknown bot token")

        message = request.data["message"]
        chat = message["chat"]
        user = message["from"]
        text = message["text"]

        bot_response = "Товарищ"
        if user.get("first_name"):
            bot_response += " " + user["first_name"]
        if user.get("last_name"):
            bot_response += " " + user["last_name"]
        if user.get("username"):
            bot_response += " " + user["username"]

        bot_response += "!\n"

        bot_response += (
            f"Вот ты пишешь:\n\n_{text!r}_\n\n- вот ты что этим хочешь сказать?"
        )

        tg_resp = self.bot_respond(chat, message, bot_response)

        return Response(
            data={
                "chat": chat["id"],
                "message": text,
                "ok": True,
                "status": tg_resp.status_code,
                "tg": tg_resp,
                "user": (
                    f"id={user.get('id')},"
                    f"fn={user.get('first_name')}, "
                    f"username={user.get('username')}"
                ),
            },
            content_type="application/json",
        )
