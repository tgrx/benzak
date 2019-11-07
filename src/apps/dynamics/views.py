from collections import defaultdict
from datetime import date

from django.db.models import Model
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormView

from apps.dynamics.forms import SearchForm
from apps.dynamics.models import PriceHistory
from project.utils import aname


class DynamicsView(FormView, ListView):
    http_method_names = {"get", "post"}
    template_name = "dynamics/index.html"
    model = PriceHistory

    def get_form_class(self):
        return SearchForm

    def get_initial(self):
        return {aname(PriceHistory.at): date.today()}

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

        history = PriceHistory.objects.all()

        # TODO: walrus op
        for field in form.fields:
            value = form.cleaned_data[field]
            if value:
                history = history.filter(**{field: value})

        grouped = defaultdict(list)
        for h in history:
            grouped[h.fuel].append(h)

        return grouped.items()

    def get_context_data(self, **kwargs):
        context = {}

        context.update(FormView.get_context_data(self, **kwargs))
        context.update(ListView.get_context_data(self, **kwargs))

        return context
