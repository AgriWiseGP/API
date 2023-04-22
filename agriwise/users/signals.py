from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from agriwise.agriculture_specialist.models import AgricultureSpecialist


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_agriculture_spcialist_instance_when_user_updated(
    sender, instance, created, *args, **kwargs
):
    if not created and instance.is_agriculture_specialist:
        AgricultureSpecialist.objects.get_or_create(user=instance)
