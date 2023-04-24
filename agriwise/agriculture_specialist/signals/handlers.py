import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from agriwise.agriculture_specialist.models import ProfileUpgradeApplication


def _delete_document_file(path):
    if os.path.isfile(path):
        os.remove(path)


@receiver(pre_delete, sender=ProfileUpgradeApplication)
def delete_document_file(sender, instance, *args, **kwargs):
    if instance.documents:
        _delete_document_file(instance.documents.path)
