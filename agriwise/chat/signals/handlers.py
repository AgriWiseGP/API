from django.db.models.signals import post_save
from django.dispatch import receiver

from agriwise.chat.models import Chat, ContactRequest


@receiver(post_save, sender=ContactRequest)
def create_chat_on_contact_request_acception(
    sender, instance, created, *args, **kwargs
):
    if not created and instance.status == "ACCEPTED":
        Chat.objects.get_or_create(user=instance.sender, specialist=instance.receiver)
