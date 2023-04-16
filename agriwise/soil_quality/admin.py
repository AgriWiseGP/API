from django.contrib import admin

from agriwise.soil_quality.models import (
    SoilElement,
    SoilQuality,

)


@admin.register(SoilQuality)
class CropAdmin(admin.ModelAdmin):
    list_display = ["quality", "created_at", "soil_elements", "user"]


@admin.register(SoilElement)
class ElemetAdmin(admin.ModelAdmin):
    list_display = ["n", "p", "k"]
