from collections import defaultdict
from datetime import date

from django.db.models import Model
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, ListView

from dynamics.forms import SearchForm
from dynamics.models import PriceHistory


class DynamicsView(ListView, FormView):
    form_class = SearchForm
    model = PriceHistory
    template_name = "dynamics/index.html"

    def get(self, request, *args, **kwargs):
        form_attrs = {_k: _v for _k, _v in kwargs.items() if _v}
        if form_attrs:
            request.GET = form_attrs

        r = super().get(request, *args, **kwargs)
        return r

    def get_initial(self):
        return {"at": date.today()}

    def form_valid(self, form):
        url = reverse("dynamics")

        for field in ("at", "fuel", "currency"):
            value = form.cleaned_data.get(field) or ""
            if isinstance(value, Model):
                value = value.pk
            url += f"{value}/"

        return redirect(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.build_form()

        return context

    def build_form(self):
        if self.request.GET:
            form = SearchForm(self.request.GET)
        else:
            form = SearchForm(initial={"at": date.today()})

        return form

    def get_queryset(self):
        if not self.request.GET:
            return []

        form = SearchForm(self.request.GET)
        if not form.is_valid():
            # TODO: implement error handling
            return []

        history = super().get_queryset()

        # TODO: walrus op
        if form.cleaned_data["at"]:
            history = history.filter(at=form.cleaned_data["at"])

        # TODO: walrus op
        if form.cleaned_data["currency"]:
            history = history.filter(currency=form.cleaned_data["currency"])

        # TODO: walrus op
        if form.cleaned_data["fuel"]:
            history = history.filter(fuel=form.cleaned_data["fuel"])

        grouped = defaultdict(list)
        for h in history:
            grouped[h.fuel].append(h)

        return grouped.items()
