import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from agriwise.plant_diseases.models import PlantDisease


@receiver(pre_delete, sender=PlantDisease)
def delete_image(sender, instance, **kwargs):
    # get the path of the image file
    file_path = instance.plant_image.image.path
    # delete the file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
