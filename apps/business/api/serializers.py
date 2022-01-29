from rest_framework import serializers
from apps.business.models import Symbol

class SymbolSerializer(serializers.Serializer)
    class Meta:
        model = Symbol
        fields = '__all__'