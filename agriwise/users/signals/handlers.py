from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from agriwise.core.helpers import _delete_image


@receiver(pre_delete, sender=get_user_model())
def delete_user_image_on_delete(sender, instance, *args, **kwargs):
    if instance.image:
        _delete_image(instance.image.path)
