from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from djoser import utils
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer

token_generator = PasswordResetTokenGenerator()
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


class EmailActivation(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user_id = utils.decode_uid(kwargs["uid"])
        user = User.objects.get(id=user_id)
        if user:
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response(
                    {"email": "Account Successfully Activated"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"email": "Account is Already Activated"},
                status=status.HTTP_400_BAD_REQUEST,
            )
