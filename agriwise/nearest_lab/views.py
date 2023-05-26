from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Location, NurersuryLocation
from .serializers import LocationSerializer, NurersuryLocationSerializer


class SupplierLocationList(APIView):
    def post(self, request):
        queryset = Location.objects.all()
        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NurseryLocationList(APIView):
    def post(self, request):
        queryset = NurersuryLocation.objects.all()
        serializer = NurersuryLocationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
