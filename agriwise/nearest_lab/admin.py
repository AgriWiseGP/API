from django.contrib import admin

from .models import Location, NurersuryLocation


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "long", "lat"]


@admin.register(NurersuryLocation)
class NurersuryLocationAdmin(admin.ModelAdmin):
    list_display = ["name", "long", "lat"]
