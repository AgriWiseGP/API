from rest_framework import serializers

from .models import Chat, ContactRequest, Message


class ContactRequestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ["id", "sender", "receiver", "status"]
        read_only_fields = ["id", "sender", "status"]


class ContactRequestSpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ["id", "sender", "receiver", "status"]
        read_only_fields = ["id", "sender", "receiver"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "send_at", "media", "subject", "chat"]
        read_only_fields = ["id", "send_at"]
        extra_kwags = {"sender": {"required": False}, "receiver": {"required": False}}


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ["id", "specialist", "user", "messages", "created_at"]
        read_only_filds = ["id", "created_at"]
