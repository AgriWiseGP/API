from django.db import transaction
from django.db.utils import InternalError
from rest_framework.serializers import ModelSerializer

from agriwise.soil_fertilizer.models import (
    SoilAnalysis,
    SoilFertilizer,
    WeatherConditions,
)


class WeatherConditionsSerializer(ModelSerializer):
    class Meta:
        model = WeatherConditions
        fields = ["temperature", "humidity", "rainfall"]


class SoilAnalysisSerializer(ModelSerializer):
    class Meta:
        model = SoilAnalysis
        fields = ["Pratio", "Kratio", "Nratio", "PH"]


class SoilFertilizerSerializer(ModelSerializer):
    soil_analysis = SoilAnalysisSerializer()
    weather_conditions = WeatherConditionsSerializer()

    class Meta:
        model = SoilFertilizer
        fields = [
            "id",
            "crop_name",
            "soil_name",
            "target",
            "created_at",
            "user",
            "soil_analysis",
            "weather_conditions",
        ]
        extra_kwargs = {"user": {"required": False}, "target": {"required": False}}
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        try:
            with transaction.atomic():
                soil_analysis_data = validated_data.pop("soil_analysis")
                weather_conditions_data = validated_data.pop("weather_conditions")
                soil_analysis = SoilAnalysis.objects.create(**soil_analysis_data)
                weather_conditions = WeatherConditions.objects.create(
                    **weather_conditions_data
                )
                soil_fertilizer = SoilFertilizer.objects.create(
                    soil_analysis=soil_analysis,
                    weather_conditions=weather_conditions,
                    **validated_data
                )
        except InternalError as e:
            raise e("An Error occured during the adding process.")
        return soil_fertilizer
