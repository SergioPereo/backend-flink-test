from django.urls import path
from apps.business.api.api import CompaniesData

urlpatterns = [
    path('companies/', CompaniesData.as_view(), name='business_data'),
]