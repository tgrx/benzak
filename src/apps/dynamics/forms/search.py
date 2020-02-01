from django import forms

from apps.dynamics.models import Currency
from apps.dynamics.models import Fuel


class SearchForm(forms.Form):
    at = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), required=False)
    fuel = forms.ModelChoiceField(queryset=Fuel.objects.all(), required=False)
