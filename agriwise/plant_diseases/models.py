from django.db import models
from django.db.models import DateTimeField, ForeignKey, ImageField

from agriwise.users.models import User


class PlantImage(models.Model):
    image = ImageField(upload_to="plant-diseases/")


class PlantDisease(models.Model):
    disease = models.CharField(max_length=200)
    created_at = DateTimeField(auto_now=True)
    plant_image = ForeignKey(PlantImage, on_delete=models.CASCADE, null=True)
    user = ForeignKey(User, on_delete=models.CASCADE, null=True)
