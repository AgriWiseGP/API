from django.db.models import Q
from django.http import Http404
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message as FirebaseMessage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chat, ContactRequest, Message
from .permissions import IsChatMember
from .serializers import (
    ChatSerializer,
    ContactRequestSpecialistSerializer,
    ContactRequestUserSerializer,
    MessageSerializer,
)


class ContactRequestView(APIView):
    def get(self, request, *args, **kwargs):
        requests = ContactRequest.objects.filter(
            Q(receiver=self.request.user.id) | Q(sender=self.request.user.id)
        )
        serializer = ContactRequestUserSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if self.request.user.is_agriculture_specialist:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        data = request.data
        data["sender"] = self.request.user.id
        serializer = ContactRequestUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContactRequestDetailView(APIView):
    def get_object(self, pk):
        try:
            return ContactRequest.objects.get(pk=pk)
        except Exception:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        contact_request = self.get_object(pk)
        serializer = ContactRequestUserSerializer(contact_request)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        if not request.user.is_agriculture_specialist:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        contact_request = self.get_object(pk)
        serializer = ContactRequestSpecialistSerializer(
            contact_request, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class ChatView(APIView):
    permissions = [IsChatMember]

    def get(self, *args, **kwargs):
        chats = Chat.objects.prefetch_related("messages").filter(
            Q(specialist=self.request.user.id) | Q(user=self.request.user.id)
        )
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)


class ChatDetailsView(APIView):
    permissions = [IsChatMember]

    def get_object(self, pk):
        try:
            return Chat.objects.prefetch_related("messages").get(pk=pk)
        except Exception:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        chat = self.get_object(pk)
        serializer = ChatSerializer(chat)
        return Response(serializer.data)

    def delete(self, requet, pk, *args, **kwargs):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageView(APIView):
    def get_chat(self, pk):
        try:
            return Chat.objects.get(pk=pk)
        except Exception:
            raise Http404

    def post(self, request, *args, **kwargs):
        data = request.data
        data._mutable = True
        chat = self.get_chat(data.get("chat"))
        data["sender"] = self.request.user.id
        data["receiver"] = chat.user.id
        if request.user.id == chat.user.id:
            data["receiver"] = chat.specialist.id
        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # send message fire base notification
        devices = FCMDevice.objects.filter(user=request.user)
        devices.send_message(FirebaseMessage(data=serializer.data))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageDetailView(APIView):
    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Exception:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        message = self.get_object(pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
