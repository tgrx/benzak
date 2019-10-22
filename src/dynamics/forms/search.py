from django import forms as f

from dynamics.models import Currency, Fuel


class SearchForm(f.Form):
    at = f.DateField(widget=f.DateInput(attrs={"type": "date"}))
    currency = f.ModelChoiceField(queryset=Currency.objects.all(), required=False)
    fuel = f.ModelChoiceField(queryset=Fuel.objects.all(), required=False)
