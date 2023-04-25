import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from agriwise.soil_type.models import SoilType


@receiver(pre_delete, sender=SoilType)
def delete_image(sender, instance, **kwargs):
    # get the path of the image file
    file_path = instance.soil_image.image.path
    # delete the file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
