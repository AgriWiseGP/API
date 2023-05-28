from django.conf import settings
from django.db import models


class ProfileUpgradeApplication(models.Model):
    STATUS = [
        ("A", "Accepted"),
        ("P", "Pending"),
        ("R", "Rejected"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    documents = models.FileField(upload_to="users/profile/upgard/")
    status = models.CharField(choices=STATUS, max_length=1, default="P")
    admin_comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
