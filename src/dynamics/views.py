from django.views.generic import TemplateView

from dynamics.models import Currency, Fuel


class DynamicsView(TemplateView):
    http_method_names = ("get", "post")

    template_name = "dynamics/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["currency"] = Currency.objects.all()
        context["fuels"] = Fuel.objects.all()

        return context
