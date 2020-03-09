from collections import defaultdict
from datetime import date

from django.db import connection
from django.db.models import Model
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormView

from apps.dynamics.forms import SearchForm
from apps.dynamics.models import Currency
from apps.dynamics.models import Fuel
from apps.dynamics.models import PriceHistory
from project.utils import a


class DynamicsView(FormView, ListView):
    http_method_names = {"get", "post"}
    template_name = "dynamics/index.html"
    model = PriceHistory

    def get_form_class(self):
        return SearchForm

    def get_initial(self):
        return {a(PriceHistory.at): date.today()}

    def get_form_kwargs(self):
        data = self.get_initial()

        for field in self.get_form_class().declared_fields:
            value = self.kwargs.get(field)
            if value:
                data[field] = value

        if self.request.POST:
            data.update(
                {
                    k: (v[0] if isinstance(v, list) else v)
                    for k, v in self.request.POST.items()
                }
            )

        return {"data": data}

    def get_success_url(self):
        def _l(_field):
            _form = self.get_form()
            _form.full_clean()
            _value = _form.cleaned_data.get(_field)
            _retvalue = None

            if isinstance(_value, Model):
                _retvalue = _value.pk
            else:
                _retvalue = _value

            return str(_retvalue or "")

        parts_fields = ("at", "fuel", "currency")

        parts = [_l(_f) for _f in parts_fields]
        parts = "/".join(parts)
        if parts:
            parts += "/"

        url = f"{reverse('dynamics')}{parts}"

        return url

    def get_queryset(self):
        form = self.get_form()
        if not form.is_valid():
            # TODO: implement error handling
            return []

        if form.cleaned_data[a(PriceHistory.at)] <= date.today():
            result = self._build_historic(form)
        else:
            result = self._predict(form)

        return result.items()

    def get_context_data(self, **kwargs):
        context = {}

        context.update(FormView.get_context_data(self, **kwargs))
        context.update(ListView.get_context_data(self, **kwargs))

        return context

    def _build_historic(self, form):
        history = PriceHistory.objects.all()

        for field in form.fields:
            value = form.cleaned_data[field]
            if value:
                history = history.filter(**{field: value})

        grouped = defaultdict(list)
        for h in history:
            grouped[h.fuel].append(h)

        return grouped

    def _predict(self, form):
        at = form.cleaned_data[a(PriceHistory.at)]

        query = f"""
            WITH
                future AS (SELECT '{at.strftime("%Y-%m-%d")}'::date AS at)
            SELECT
                at,
                fuel_id,
                round(regr_intercept(y, x)::numeric, 2) AS price
            FROM
                (SELECT
                     future.at                                                          AS at,
                     f.id                                                               AS fuel_id,
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
                fuel_id, at
            ;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            raw_prices = [dict(zip(columns, row)) for row in rows]

        byn = Currency.objects.get(name="BYN")

        grouped = defaultdict(list)
        for rp in raw_prices:
            fuel = Fuel.objects.get(pk=rp["fuel_id"])
            grouped[fuel].append(
                {"at": rp["at"], "price": rp["price"], "currency": byn}
            )

        return grouped
