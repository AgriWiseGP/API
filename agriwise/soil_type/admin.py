from django.contrib import admin

from agriwise.soil_type.models import SoilImage, SoilType


@admin.register(SoilType)
class SoilTypeAdmin(admin.ModelAdmin):
    list_display = ["soil_type", "created_at", "user", "soil_image"]


@admin.register(SoilImage)
class SoilImageAdmin(admin.ModelAdmin):
    list_display = ["image"]
