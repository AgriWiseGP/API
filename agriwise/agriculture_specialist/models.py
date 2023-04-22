from django.conf import settings
from django.db import models


class AgricultureSpecialist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rate = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class ProfileUpgradeApplication(models.Model):
    STATUS = [
        ("A", "Acepted"),
        ("P", "Pending"),
        ("R", "Rejected"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    documents = models.FileField(upload_to=f"users/profile/upgrade/{user.name}/")
    status = models.CharField(choices=STATUS, max_length=1, default="P")
    admin_comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
