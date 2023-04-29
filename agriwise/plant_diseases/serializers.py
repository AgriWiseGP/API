from rest_framework import serializers

from .models import PlantDisease, PlantImage


class PlantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantImage
        fields = "__all__"


class PlantDiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantDisease
        fields = "__all__"
        read_only_fields = ["id", "created_at", "user", "disease", "plant_image"]
