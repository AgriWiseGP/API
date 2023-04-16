from rest_framework import serializers

from agriwise.soil_quality.models import SoilElement, SoilQuality


class SoilAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilElement
        fields = "__all__"


class SoilQualitySerializer(serializers.ModelSerializer):
    soil_elements = SoilAnalysisSerializer()
    quality = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SoilQuality
        fields = ["id", "quality", "user", "created_at", "soil_elements"]

    def create(self, validated_data):
        soil_elements_data = validated_data.pop("soil_elements")
        soil_elements = SoilElement.objects.create(**soil_elements_data)

        soil_quality = SoilQuality.objects.create(
            soil_elements=soil_elements, **validated_data
        )
        return soil_quality
