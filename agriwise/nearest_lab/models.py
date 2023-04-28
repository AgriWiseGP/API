from django.db import models
from django.db.models import FloatField, ForeignKey

from agriwise.users.models import User


class Location(models.Model):
    long = FloatField()
    lat = FloatField()
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True)
