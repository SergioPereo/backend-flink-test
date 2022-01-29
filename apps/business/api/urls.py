from django.urls import path
from apps.business.api.api import CompaniesData, Symbols

urlpatterns = [
    path('companies/', CompaniesData.as_view(), name='business_data_companies'),
    path('symbols/', Symbols.as_view(), name='business_data_symbols')
]