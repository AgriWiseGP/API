from rest_framework.serializers import ModelSerializer

from .models import ProfileUpgradeApplication


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
