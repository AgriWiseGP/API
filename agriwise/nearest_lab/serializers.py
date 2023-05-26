from rest_framework import serializers

from .models import Location, NurersuryLocation


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class NurersuryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurersuryLocation
        fields = "__all__"
