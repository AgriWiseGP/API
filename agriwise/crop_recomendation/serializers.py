from rest_framework import serializers
from .models import SoilElement, CropRecommendation

class SoilElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilElement
        fields = '__all__'

class CropRecommendationSerializer(serializers.ModelSerializer):
    soil_elements = serializers.PrimaryKeyRelatedField(queryset=SoilElement.objects.all())
    class Meta:
        model = CropRecommendation
        fields = '__all__'

