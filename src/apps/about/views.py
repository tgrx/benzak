from django.views.generic import ListView

from apps.about.models import Technology


class AboutView(ListView):
    template_name = "about/index.html"
    model = Technology
