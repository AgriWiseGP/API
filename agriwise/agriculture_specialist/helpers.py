from django.core.mail import EmailMessage
from rest_framework.exceptions import APIException


def send_email(subject, message, recipient_list):
    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            to=recipient_list,
        )
        email.send()
    except Exception as e:
        raise APIException(detail=str(e))
