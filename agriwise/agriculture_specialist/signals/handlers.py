import os

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from agriwise.agriculture_specialist.models import ProfileUpgradeApplication


def _delete_document_file(path):
    if os.path.isfile(path):
        os.remove(path)


@receiver(pre_delete, sender=ProfileUpgradeApplication)
def delete_document_file(sender, instance, *args, **kwargs):
    if instance.documents:
        _delete_document_file(instance.documents.path)


@receiver(post_save, sender=ProfileUpgradeApplication)
def update_user_on_application_acceptance(sender, instance, *args, **kwargs):
    if not kwargs["created"]:
        if instance.status == "A":
            user = (
                get_user_model()
                .objects.filter(profileupgradeapplication=instance.id)
                .first()
            )
            user.is_agriculture_specialist = True
            user.save()
            # sending acceptance email to the user

        elif instance.status == "R":
            # sending reject email to the user
            pass
