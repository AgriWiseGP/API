from django.core.mail import EmailMessage
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

def send_email(subject, message, recipient_list):
    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            to=recipient_list,
        )
        email.send()
        return Response({"message": "Email sent successfully."}, status=HTTP_200_OK)
    except Exception as e:
        raise APIException(detail=str(e), code=HTTP_400_BAD_REQUEST)