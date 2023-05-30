from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class WeatherData(models.Model):
    location = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)


class Plant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cultivation_requirements = models.TextField()


class Crop(models.Model):
    name = models.CharField(max_length=100)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    yields = models.FloatField()
    growth_stage = models.CharField(max_length=50)
    harvest_date = models.DateField()
