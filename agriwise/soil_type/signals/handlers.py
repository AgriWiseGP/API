import os

from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver

from agriwise.soil_type.models import SoilType


@receiver(pre_delete, sender=SoilType)
def delete_image(sender, instance, **kwargs):
    # get the path of the image file
    file_path = instance.soil_image.image.path
    # delete the file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)


@receiver(post_delete, sender=SoilType)
def delete_soil_image(sender, instance, **kwargs):
    if instance.soil_image:
        instance.soil_image.delete()
