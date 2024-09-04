from rest_framework import serializers
from .models import Calculation

class CalculationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calculation
        fields = '__all__'



class CalculationRequestSerializer(serializers.Serializer):
    first_month = serializers.CharField()
    last_month = serializers.CharField()
    given_money = serializers.IntegerField()

class CalculationResponseSerializer(serializers.Serializer):
    asset = serializers.CharField()
    profit = serializers.FloatField()
    percentage = serializers.FloatField()