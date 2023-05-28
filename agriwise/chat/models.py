import uuid

from django.conf import settings
from django.db import models


class ContactRequest(models.Model):
    status = [
        ("ACCEPTED", "ACCEPTED"),
        ("PENDING", "PENDING"),
        ("REJECTED", "REJECTED"),
    ]
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contact_request_sender",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contact_request_receiver",
    )
    status = models.CharField(max_length=20, choices=status, default="PENDING")


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_user"
    )
    specialist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_specialist",
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="message_sender",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="message_receiver",
    )
    subject = models.TextField(null=True, blank=True)
    media = models.FileField(null=True, blank=True, upload_to="messages/")
    send_at = models.DateTimeField(auto_now_add=True)
