from django.urls import path
from .views import calculate_for_given_asset, calculate_for_given_months, CalculationList, CalculateForGivenMonthsView, CalculateForGivenAssetView

urlpatterns = [
    path('calculate-for-given-asset/<str:asset_name>/<int:user_id>/', calculate_for_given_asset, name='calculate-for-given-asset'),
    path('calculate-for-given-months/', calculate_for_given_months, name='calculate-for-given-months'),
    path('calculation-list/', CalculationList.as_view(), name='calculation-list'),
    path('calculate-for-given-months-view/', CalculateForGivenMonthsView.as_view(), name='calculate-for-given-months-view-class-based'),
    path('max-profit-response-serializer/', CalculateForGivenAssetView.as_view(), name='max-profit-response-serializer-class-based'),

]