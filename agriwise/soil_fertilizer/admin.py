from django.contrib import admin

from agriwise.soil_fertilizer.models import (
    SoilAnalysis,
    SoilFertilizer,
    WeatherConditions,
)

admin.site.register(SoilFertilizer)
admin.site.register(SoilAnalysis)
admin.site.register(WeatherConditions)
