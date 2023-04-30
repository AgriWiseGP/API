from django.db import models
from django.db.models import DateTimeField, ForeignKey, ImageField

from agriwise.users.models import User


class SoilImage(models.Model):
    image = ImageField(upload_to="soil-type/")


class SoilType(models.Model):
    soil_type = models.CharField(max_length=200)
    created_at = DateTimeField(auto_now=True)
    soil_image = ForeignKey(SoilImage, on_delete=models.SET_NULL, null=True)
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True)
