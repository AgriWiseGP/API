from django.conf import settings
from django.db import models


class SoilAnalysis(models.Model):
    Pratio = models.DecimalField(max_digits=7, decimal_places=2)
    Kratio = models.DecimalField(max_digits=7, decimal_places=2)
    Nratio = models.DecimalField(max_digits=7, decimal_places=2)
    PH = models.DecimalField(max_digits=7, decimal_places=2)


class WeatherConditions(models.Model):
    temperature = models.DecimalField(max_digits=7, decimal_places=2)
    humidity = models.DecimalField(max_digits=7, decimal_places=2)
    rainfall = models.DecimalField(max_digits=7, decimal_places=2)


class SoilFertilizer(models.Model):
    soils = [
        ("Clayey", "Clayey"),
        ("alluvial", "alluvial"),
        ("clay loam", "clay loam"),
        ("coastal", "coastal"),
        ("laterite", "laterite"),
        ("sandy", "sandy"),
        ("silty clay", "silty clay"),
    ]

    crops = [
        ("rice", "rice"),
        ("Coconut", "Coconut"),
    ]

    crop_name = models.CharField(max_length=100, choices=crops)
    soil_name = models.CharField(max_length=100, choices=soils)
    target = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    soil_analysis = models.ForeignKey(
        SoilAnalysis, related_name="+", on_delete=models.CASCADE
    )
    weather_conditions = models.ForeignKey(
        WeatherConditions, related_name="+", on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " " + self.soil_name + " soil for " + self.crop_name
