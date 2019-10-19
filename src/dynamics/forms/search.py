from django import forms as f

from dynamics.models import Currency, Fuel, PriceHistory


class SearchForm(f.ModelForm):
    currency = f.ModelChoiceField(queryset=Currency.objects.all(), required=False)
    fuel = f.ModelChoiceField(queryset=Fuel.objects.all(), required=False)

    class Meta:
        model = PriceHistory
        fields = ("at", "currency", "fuel")
        widgets = {"at": f.DateInput(attrs={"type": "date"})}
