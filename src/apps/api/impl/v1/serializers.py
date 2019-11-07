from rest_framework import serializers

from apps.dynamics.models import Currency, Fuel, PriceHistory


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuel
        fields = "__all__"


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = "__all__"


class DynamicsPriceSerializer(serializers.Serializer):
    currency = CurrencySerializer(read_only=True)
    value = serializers.DecimalField(read_only=True, max_digits=24, decimal_places=2)


class DynamicsFuelSerializer(serializers.Serializer):
    fuel = FuelSerializer(read_only=True)
    prices = serializers.ListField(
        child=DynamicsPriceSerializer(read_only=True), read_only=True
    )


class DynamicsSerializer(serializers.Serializer):
    at = serializers.DateField(read_only=True)
    fuels = serializers.ListField(
        child=DynamicsFuelSerializer(read_only=True), read_only=True
    )
