from django.urls import path

from .views import (
    ChatDetailsView,
    ChatView,
    ContactRequestDetailView,
    ContactRequestView,
    MessageDetailView,
    MessageView,
)

urlpatterns = [
    path("contact-request/", ContactRequestView.as_view()),
    path("contact-request/<int:pk>", ContactRequestDetailView.as_view()),
    path("chat/", ChatView.as_view()),
    path("chat/<uuid:pk>", ChatDetailsView.as_view()),
    path("message/", MessageView.as_view()),
    path("message/<uuid:pk>", MessageDetailView.as_view()),
]
