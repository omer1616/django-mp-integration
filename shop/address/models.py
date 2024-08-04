from django.db import models
from shop.utils.models import StartedModel


class Country(StartedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)


class City(StartedModel):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')


class Township(StartedModel):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='township')


# Create your models here.
class Address(StartedModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    township = models.ForeignKey(Township, on_delete=models.CASCADE)
    full_address = models.TextField()




