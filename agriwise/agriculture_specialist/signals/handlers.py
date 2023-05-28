from django.db.models.signals import pre_delete
from django.dispatch import receiver

from agriwise.agriculture_specialist.models import ProfileUpgradeApplication
from agriwise.core.helpers import _delete_document_file


@receiver(pre_delete, sender=ProfileUpgradeApplication)
def delete_document_file(sender, instance, *args, **kwargs):
    if instance.documents:
        _delete_document_file(instance.documents.path)
