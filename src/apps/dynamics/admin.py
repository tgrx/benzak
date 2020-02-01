from django import forms
from django.contrib import admin
from django.db import models

from apps.dynamics.models import Currency
from apps.dynamics.models import Fuel
from apps.dynamics.models import PriceHistory


class FuelModelAdminForm(forms.ModelForm):
    class Meta:
        model = Fuel
        fields = "__all__"
        widgets = {"color": forms.TextInput(attrs={"type": "color"})}


@admin.register(Currency)
class CurrencyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {"widget": forms.TextInput}}


@admin.register(Fuel)
class FuelModelAdmin(admin.ModelAdmin):
    form = FuelModelAdminForm
    formfield_overrides = {models.TextField: {"widget": forms.TextInput}}


@admin.register(PriceHistory)
class PriceHistoryModelAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {"widget": forms.TextInput}}
