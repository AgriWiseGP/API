import os

from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver

from agriwise.plant_diseases.models import PlantDisease


@receiver(pre_delete, sender=PlantDisease)
def delete_media_image(sender, instance, **kwargs):
    # get the path of the image file
    file_path = instance.plant_image.image.path
    # delete the file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)


# used post_delete to avoid maximum recursion depth exceeded error when deleting related model instances
@receiver(post_delete, sender=PlantDisease)
def delete_plant_image(sender, instance, **kwargs):
    if instance.plant_image:
        instance.plant_image.delete()
