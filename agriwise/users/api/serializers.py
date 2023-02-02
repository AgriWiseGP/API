from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class UserCreateSerializer(BaseUserCreateSerializer):
    email = serializers.EmailField(required=True)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["id", "username", "password", "email"]
