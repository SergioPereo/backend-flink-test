from django.db import models
import uuid

# Create your models here.

class Company(models.Model):
    def get_market_values(self):
        return MarketValue.objects.filter(company=self.id)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    symbol = models.CharField(max_length=50)


class MarketValue(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    value = models.DecimalField(max_digits=14, decimal_places=2)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

class Symbol(models.Model):
    value = models.CharField(max_length=50)