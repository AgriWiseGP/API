from django.contrib import admin

from .models import CropRecommendation, SoilElement


@admin.register(CropRecommendation)
class CropAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "soil_elements", "user"]


@admin.register(SoilElement)
class ElemetAdmin(admin.ModelAdmin):
    list_display = ["n", "p", "k"]
