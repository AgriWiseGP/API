from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from .models import ProfileUpgradeApplication

User = get_user_model()


class ProfileUpgradeApplicationAdminSerializer(ModelSerializer):
    class Meta:
        model = ProfileUpgradeApplication
        fields = [
            "id",
            "user",
            "documents",
            "status",
            "admin_comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "documents", "created_at", "updated_at"]


class ProfileUpgradeApplicationUserSerializer(ModelSerializer):
    class Meta:
        model = ProfileUpgradeApplication
        fields = [
            "id",
            "user",
            "documents",
            "status",
            "admin_comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "admin_comment",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"user": {"required": False}}


class AgricultureSpecialistSerializer(ModelSerializer):
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
