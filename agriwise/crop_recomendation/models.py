from django.db import models
from django.db.models import CharField, DateTimeField, FloatField, ForeignKey

from agriwise.users.models import User


class SoilElement(models.Model):
    n = FloatField()
    p = FloatField()
    k = FloatField()
    temperature = FloatField()
    humidity = FloatField()
    ph = FloatField()
    rainfall = FloatField()

    def __str__(self):
        return f"SoilElements({self.n}, {self.p}, {self.k}, {self.temperature})"


class CropRecommendation(models.Model):
    name = CharField(max_length=100)
    created_at = DateTimeField(auto_now=True)
    soil_elements = ForeignKey(SoilElement, on_delete=models.CASCADE)
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True)
