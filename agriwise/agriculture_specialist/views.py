from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from agriwise.core.permissions import IsOwnerUser

from .models import ProfileUpgradeApplication
from .serializers import ProfileUpgradeApplicationUserSerializer


class ProfileUpgradeAdminView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        pass


class ProfileUpgradeAdminDetailsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass


class ProfileUpgradeUserView(APIView):
    permission_classes = [IsOwnerUser]

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
    permission_classes = [IsOwnerUser]

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
