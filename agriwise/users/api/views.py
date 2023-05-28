from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from agriwise.core.permissions import IsOwnerUser

from .serializers import PasswordChangeSerializer, UserDetailsSerializer, UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UserDetailsView(APIView):
    permission_classes = [IsOwnerUser]

    def get(self, request, *args, **kwargs):
        user_serializer = UserDetailsSerializer(request.user)
        return Response(user_serializer.data)

    def put(self, request, *args, **kwargs):
        user_serializer = UserDetailsSerializer(request.user, data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_202_ACCEPTED)


class UsersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(
            ~Q(id=request.user.id) & Q(is_agriculture_specialist=False)
        )
        users_serializer = UserDetailsSerializer(users, many=True)
        return Response(users_serializer.data)


class UserDetailsForOtherUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except Exception:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        print(pk)
        user = self.get_object(pk)
        user_serializer = UserDetailsSerializer(user)
        return Response(user_serializer.data)


class PasswordChangeView(APIView):
    permission_classes = [IsOwnerUser]

    def put(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Password updated successfully."},
            status=status.HTTP_202_ACCEPTED,
        )
