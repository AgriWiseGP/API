from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from agriwise.core.permissions import IsOwnerUser

from .models import ProfileUpgradeApplication
from .serializers import (
    AgricultureSpecialistSerializer,
    ProfileUpgradeApplicationAdminSerializer,
    ProfileUpgradeApplicationUserSerializer,
)

User = get_user_model()


class ProfileUpgradeAdminView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        applications = ProfileUpgradeApplication.objects.filter(status="P")
        application_serializer = ProfileUpgradeApplicationAdminSerializer(
            applications, many=True
        )
        return Response(application_serializer.data)


class ProfileUpgradeAdminDetailsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_pending_application_with_pk(self, pk):
        try:
            return ProfileUpgradeApplication.objects.get(status="P", pk=pk)
        except Exception:
            raise Http404("Pending application with the given id is not found.")

    def get(self, request, pk, *args, **kwargs):
        application = self.get_pending_application_with_pk(pk)
        application_serializer = ProfileUpgradeApplicationAdminSerializer(application)
        return Response(application_serializer.data)

    def put(self, request, pk, *args, **kwargs):
        application = self.get_pending_application_with_pk(pk)
        application_serializer = ProfileUpgradeApplicationAdminSerializer(
            application, data=request.data
        )
        application_serializer.is_valid(raise_exception=True)
        application_serializer.save()
        if application_serializer.data["status"] == "A":
            user = (
                get_user_model()
                .objects.filter(profileupgradeapplication=application.id)
                .first()
            )
            user.is_agriculture_specialist = True
            user.save()
        return Response(application_serializer.data, status=status.HTTP_202_ACCEPTED)


class ProfileUpgradeUserView(APIView):
    permission_classes = [IsOwnerUser, permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_applications = ProfileUpgradeApplication.objects.filter(
            user=request.user.id
        )
        application_serializer = ProfileUpgradeApplicationUserSerializer(
            user_applications, many=True
        )
        return Response(application_serializer.data)

    def post(self, request, *args, **kwargs):
        application_serializer = ProfileUpgradeApplicationUserSerializer(
            data={"user": request.user.id, "documents": request.data["documents"]}
        )
        application_serializer.is_valid(raise_exception=True)
        application_serializer.save()
        return Response(application_serializer.data, status=status.HTTP_201_CREATED)


class ProfileUpgradeUserDetailsView(APIView):
    permission_classes = [IsOwnerUser, permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        application = get_object_or_404(ProfileUpgradeApplication, pk=pk)
        application_serializer = ProfileUpgradeApplicationUserSerializer(application)
        return Response(application_serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        application = get_object_or_404(ProfileUpgradeApplication, pk=pk)
        application.delete()
        return Response(
            {"message": "Application is deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class AgricultureSpecialistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        specialists = User.objects.filter(is_agriculture_specialist=True)
        specialists_serializer = AgricultureSpecialistSerializer(specialists, many=True)
        return Response(specialists_serializer.data)


class AgricultureSpecialistDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except Exception:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        print(pk)
        specialist = self.get_object(pk)
        specialist_serializer = AgricultureSpecialistSerializer(specialist)
        return Response(specialist_serializer.data)
