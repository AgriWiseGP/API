from rest_framework import serializers

from .models import SoilImage, SoilType


class SoilImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilImage
        fields = "__all__"


class SoilTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilType
        fields = "__all__"
        read_only_fields = ["id", "created_at", "user", "soil_type", "soil_image"]
