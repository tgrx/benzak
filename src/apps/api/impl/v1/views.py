from datetime import date
from datetime import datetime
from datetime import timedelta
from decimal import Decimal
from typing import Dict
from typing import NamedTuple
from typing import Optional
from typing import Tuple

import requests
from django.db import IntegrityError
from django.db import connection
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
from project.utils import a


class EstimateT(NamedTuple):
    fuel: str
    price: Optional[Decimal]


class PredictionT(NamedTuple):
    at: date
    estimates: Tuple[EstimateT]


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
    def get_actual_prices(self):
        fuels = Fuel.objects.all()
        currency = Currency.objects.filter(name="BYN").first()

        prices = []

        n = datetime.now().date()

        for fuel in fuels:
            ph: PriceHistory = PriceHistory.objects.filter(
                fuel=fuel, currency=currency
            ).order_by("-at").first()
            if ph:
                price = f"{fuel.name}: {round(ph.price, 2)} р. ({(n - ph.at).days} д.)"
                prices.append(price)

        return prices

    def predict(self, window):
        query = f"""
            WITH
                future AS (SELECT date_trunc('day', statement_timestamp() + '{window} month'::interval)::date AS at)
            SELECT
                at,
                fuel,
                round(regr_intercept(y, x)::numeric, 2) AS price
            FROM
                (SELECT
                     future.at                                                          AS at,
                     f.{a(Fuel.name)}                                                   AS fuel,
                     extract(EPOCH FROM age(ph.{a(PriceHistory.at)}, future.at))::float AS x,
                     {a(PriceHistory.price)}::float                                     AS y
                 FROM
                     future,
                     {a(Currency)} AS c,
                     {a(Fuel)} AS f,
                     {a(PriceHistory)} AS ph
                 WHERE
                       ph.{a(PriceHistory.currency_id)} = c.id
                   AND ph.{a(PriceHistory.fuel_id)} = f.id
                   AND c.{a(Currency.name)} = 'BYN'
                   AND age(statement_timestamp(), ph.{a(PriceHistory.at)}) <= age(future.at, statement_timestamp())
                ) AS historical
            GROUP BY
                fuel, at
            ;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            raw_prices = [dict(zip(columns, row)) for row in rows]

        if not raw_prices:
            return None

        raw_prices.sort(key=lambda _elm: _elm["fuel"])

        prediction = PredictionT(
            at=raw_prices[0]["at"],
            estimates=tuple(
                EstimateT(fuel=_elm["fuel"], price=_elm["price"])
                for _elm in raw_prices
                if _elm["price"]
            ),
        )

        if not prediction.estimates:
            return None

        return prediction

    def bot_respond(self, chat, reply, message_id=None, html=False):
        bot_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BENZAKBOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": chat["id"],
            "text": reply,
            "reply_markup": {
                "keyboard": [
                    [{"text": "Актуальные"}],
                    [{"text": "Прогноз на месяц"}],
                    [{"text": "Прогноз на три"}, {"text": "Прогноз на год"}],
                ],
                "resize_keyboard": True,
            },
        }

        if html:
            payload["parse_mode"] = "HTML"

        if message_id:
            payload["reply_to_message_id"] = message_id

        tg_resp = requests.post(bot_url, json=payload)

        return tg_resp

    def post(self, request: Request, *_args, **_kw):
        if not settings.TELEGRAM_BENZAKBOT_TOKEN or not request:
            raise PermissionDenied("invalid bot configuration")

        try:
            ok = self._do_post(request)
        except Exception:
            ok = False

        return Response(data={"ok": ok}, content_type="application/json")

    def _do_post(self, request):
        if "message" not in request.data:
            return False
        message = request.data["message"]
        chat = message["chat"]
        user = message["from"]
        text = message.get("text")
        if not text:
            return False
        kw = {}

        if text in ("/actual", "Актуальные"):
            bot_response = "Актуальные цены:\n\n" + "\n".join(self.get_actual_prices())
        elif text.startswith("/predict") or text.startswith("Прогноз"):
            kw["message_id"] = message["message_id"]
            window = 1
            if text.startswith("/predict"):
                window = float(text.split("/predict")[-1] or 1)
            elif text.startswith("Прогноз"):
                window = {
                    "Прогноз на месяц": 1,
                    "Прогноз на три": 3,
                    "Прогноз на год": 12,
                }[text]
            pred = self.predict(window)
            if not pred:
                at = date.today() + timedelta(days=int(30 * window))
                bot_response = f"Не могу предсказать цены на {at.strftime('%Y-%m-%d')}"
            else:
                bot_response = (
                    f"<b>Прогноз на {pred.at.strftime('%Y-%m-%d')}</b>\n\n<pre>"
                    + "\n".join(f"{e.fuel:<10}\t{e.price:.02f}" for e in pred.estimates)
                    + "</pre>\n"
                )
                kw["html"] = True
        else:
            bot_response = ""
            if user.get("username"):
                bot_response += "@" + user["username"]
            elif user.get("first_name"):
                bot_response += user["first_name"]
                if user.get("last_name"):
                    bot_response += " " + user["last_name"]

            bot_response += "! За слова ответишь?"
            kw["message_id"] = message["message_id"]

        tg_resp = self.bot_respond(chat, bot_response, **kw)
        print(tg_resp)

        return True
