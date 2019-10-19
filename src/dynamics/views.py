from collections import defaultdict
from datetime import date

from django.views.generic import ListView

from dynamics.forms import SearchForm
from dynamics.models import PriceHistory


class DynamicsView(ListView):
    http_method_names = ("get", "post")
    template_name = "dynamics/index.html"
    model = PriceHistory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm(self.request.GET, initial={"at": date.today()})

        return context

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
