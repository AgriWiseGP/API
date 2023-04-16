from django.db import models
from django.db.models import DateTimeField, FloatField, ForeignKey

from agriwise.users.models import User


class SoilElement(models.Model):
    n = FloatField()
    p = FloatField()
    k = FloatField()
    ph = FloatField()
    ec = FloatField()
    oc = FloatField()
    s = FloatField()
    zn = FloatField()
    fe = FloatField()
    cu = FloatField()
    mn = FloatField()
    b = FloatField()

    def __str__(self):
        return f"SoilElements({self.n}, {self.p}, {self.k}, {self.ph})"


class SoilQuality(models.Model):
    quality = models.CharField(max_length=100)
    created_at = DateTimeField(auto_now=True)
    soil_elements = ForeignKey(SoilElement, on_delete=models.SET_NULL, null=True)
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"SoilQualities({self.quality}, {self.user}, {self.soil_elements}, {self.created_at})"
