from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Location
from .serializers import LocationSerializer


class LocationList(APIView):
    def get(self, request, *args, **kwargs):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
