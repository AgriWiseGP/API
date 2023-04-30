import os

from agriculture_specialist.helpers import send_email
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
    user = (
        get_user_model().objects.filter(profileupgradeapplication=instance.id).first()
    )
    if not kwargs["created"]:
        if instance.status == "A":
            user.is_agriculture_specialist = True
            user.save()
            # sending acceptance email to the user
            subject = "Congratulations on Upgrading Your Account"
            message = (
                f"Dear {user.username},\n\nCongratulations on upgrading your account with us! "
                f"With your new account, you'll have access to a variety of features and capabilities "
                f"that will help you get the most out of our platform. Thank you for choosing us, and "
                f"we look forward to continuing to serve you.\n\nBest regards,\n[Agriwise Team]"
            )
            recipient_list = [user.email]
            send_email(subject=subject, message=message, recipient_list=recipient_list)

        elif instance.status == "R":
            # sending reject email to the user
            subject = "Rejection of Upgrading Your Account"
            message = (
                f"Dear {user.username},\n\nUnfortunately, We regret to inform you that we are"
                f" unable to process your request to upgrade your account at this time due to "
                f"not enough application. Please contact us for more information."
                f"\n\nBest regards,\n[Agriwise Team]"
            )
            recipient_list = [user.email]
            send_email(subject=subject, message=message, recipient_list=recipient_list)
