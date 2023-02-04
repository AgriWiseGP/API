from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

from .helper import check_password_strength

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

    def validate(self, attrs):
        if not attrs.get("email"):
            raise serializers.ValidationError(
                {"email_error", "User should have a email"}
            )

        if not attrs.get("username"):
            raise serializers.ValidationError(
                {"username_error": "User should have a username"}
            )

        if User.objects.filter(email=attrs["email"]):
            raise serializers.ValidationError(
                {"email_duplication": "This email already exists"}
            )

        if User.objects.filter(username=attrs["username"]):
            raise serializers.ValidationError(
                {"username_duplication": "This username already exists"}
            )
        if not check_password_strength(attrs.get("password")):
            raise serializers.ValidationError(
                {
                    "password_strength_error": "Password should contain at lowercase/uppercase characters and numbers"
                }
            )
        return attrs

    def create(self, validation_data):
        return User.objects.create_user(
            username=validation_data["username"],
            email=validation_data["email"],
            password=validation_data["password"],
        )
