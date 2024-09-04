from django.contrib.admin import ModelAdmin, register
from .models import Calculation


@register(Calculation)
class CalculationAdmin(ModelAdmin):
    list_display = ['user', 'asset', 'start_month', 'end_month', 'given_money', 'profit', 'percentage']

