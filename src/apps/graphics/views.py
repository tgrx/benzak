from django.views.generic import TemplateView


class GraphicsView(TemplateView):
    template_name = "graphics/index.html"
