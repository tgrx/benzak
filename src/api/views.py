import os
from base64 import b64encode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic.detail import DetailView

from api.models import ApiSettings


class ApiSettingsView(LoginRequiredMixin, DetailView):
    http_method_names = ("get",)

    template_name = "api/index.html"
    model = ApiSettings

    def get_object(self, queryset=None):
        qs = queryset if queryset is not None else self.get_queryset()
        return qs.filter(user=self.request.user).first()


class ApiResetTokenView(LoginRequiredMixin, RedirectView):
    http_method_names = ("post",)

    def get_redirect_url(self, *args, **kwargs):
        try:
            obj = get_object_or_404(ApiSettings, user=self.request.user)
        except Http404:
            obj = ApiSettings(user=self.request.user)

        obj.token = b64encode(os.urandom(256)).decode()
        obj.save()

        return reverse_lazy("api_settings")
