from django.db import models
from django.db.models import CharField, FloatField


class Location(models.Model):
    name = CharField(max_length=600)
    long = FloatField()
    lat = FloatField()
