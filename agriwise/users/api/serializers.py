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


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "username",
            "email",
            "is_agriculture_specialist",
            "image",
        ]
        read_only_fields = ["uuid", "email", "is_agriculture_specialist", "username"]
        extra_kwargs = {"name": {"required": False}, "image": {"required": False}}

        def save(self):
            name = self.validated_data.get("name", self.instance.name)
            image = self.validated_data.get("image", self.instance.image)
            self.instance.name = name
            self.instance.image = image
            self.instance.save()
            return self.instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if not check_password_strength(attrs.get("new_password")):
            raise serializers.ValidationError(
                {
                    "password_strength_error": "Password should contain at lowercase/uppercase characters and numbers"
                }
            )
        if not self.context.get("user").check_password(attrs.get("old_password")):
            raise serializers.ValidationError({"old_password_error": "Wrong Password."})
        if attrs.get("old_password") == attrs.get("new_password"):
            raise serializers.ValidationError(
                {
                    "password_error": "The old password and the new password are the same."
                }
            )
        return attrs

    def save(self):
        user = self.context.get("user")
        user.set_password(self.validated_data.get("new_password"))
        user.save()
