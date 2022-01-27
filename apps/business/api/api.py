from rest_framework.response import  Response
from rest_framework.views import APIView
from rest_framework.response import  Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from apps.business.models import Company, MarketValue
from django.core.exceptions import ValidationError


#Intente buscar una api en tiempo real, pero no lo conseguí. Sin embargo encontre un listado con los símbolos en la página https://www.nyse.com/listings_directory/stock, de ahí biene la lista
NYSE_SYMBOLS = ["A", "AA", "AAC", "AAC.U", "AACG", "AACI", "AACIU", "AACOU", "AADI", "AAIC"]

#API View para crear y indexar la información de las compañías
class CompaniesData(APIView):
    permission_classes = [AllowAny]
    #Estoy asumiendo que la información será entregada en un json con estos nombres. Y que los valores de mercado se entregaran como un string de números separados por comas
    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        symbol = request.data.get('symbol')
        market_values = request.data.get('market_values')

        if len(name) <= 50:
            if len(description) <= 100:
                if len(symbol) <= 10:
                    if symbol in NYSE_SYMBOLS:
                        market_list = market_values.split(',')
                        try:
                            values = [int(value.strip()) for value in market_list]
                        except:
                            return Response({"detail": "Error", "message": "Not value format for market_list, it must be a string with list of numbers separated by commas."}) 
                        else:
                            company = Company(name=name, description=description, symbol=symbol)
                            company.save()
                            for value in values:
                                market_value = MarketValue(value=value, company=company)
                    else:
                       return Response({"detail": "Error", "message": "This is not a registered NYSE symbol."}) 
                else:
                    return Response({"detail": "Error", "message": "Not valid format for symbol, it must be a string with no more than 100 characters."})
            else:
                return Response({"detail": "Error", "message": "Not valid format for description, it must be a string with no more than 100 characters."})
        else:
            return Response({"detail": "Error", "message": "Not valid format for name, it must be a string with no more than 50 characters."})
    def get(self, request):
        try:
            companies_information = []
            market_values = []
            count = 0
            companies = Company.objects.all()
            for company in companies:
                for market_value in company.get_market_values().order_by('id'):
                    market_values.append({"id": market_value.id, "value": market_value.value})
                companies_information.append({"id": company.id, "name": company.name, "description": company.description, "symbol": company.symbol, "values": market_values})
                market_values = []
            return Response(companies_information)
        except:
            return Response({"error": "There was an error in the request"})