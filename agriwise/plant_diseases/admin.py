from django.contrib import admin

from agriwise.plant_diseases.models import PlantDisease, PlantImage


@admin.register(PlantDisease)
class PlantDiseaseAdmin(admin.ModelAdmin):
    list_display = ["disease", "created_at", "user", "plant_image"]


@admin.register(PlantImage)
class PlantImageAdmin(admin.ModelAdmin):
    list_display = ["image"]
