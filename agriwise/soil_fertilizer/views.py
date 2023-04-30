from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from agriwise.core.permissions import IsOwnerOrReadOnly
from agriwise.soil_fertilizer.ml.soil_fertilizer_ml_model import SoilFertilizerMLModel
from agriwise.soil_fertilizer.models import SoilFertilizer
from agriwise.soil_fertilizer.serializers import SoilFertilizerSerializer


class SoilFertilizerAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        soils_fertilizer = SoilFertilizer.objects.select_related(
            "soil_analysis", "weather_conditions"
        ).filter(user=request.user)
        serializer = SoilFertilizerSerializer(soils_fertilizer, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            input_data = [
                {
                    "Temperature": data["weather_conditions"]["temperature"],
                    "Humidity": data["weather_conditions"]["humidity"],
                    "Rainfall": data["weather_conditions"]["rainfall"],
                    "pH": data["soil_analysis"]["PH"],
                    "N": data["soil_analysis"]["Nratio"],
                    "P": data["soil_analysis"]["Pratio"],
                    "K": data["soil_analysis"]["Kratio"],
                    "Soil": data["soil_name"],
                    "Crop": data["crop_name"],
                }
            ]
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        ml_model = SoilFertilizerMLModel()
        target = ml_model.compute_prediction(input_data)
        data["target"] = target
        data["user"] = request.user.id
        serializer = SoilFertilizerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SoilFertilizerDetailsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        try:
            soil_fertilizer = SoilFertilizer.objects.select_related(
                "soil_analysis", "weather_conditions"
            ).get(pk=pk)
            serializer = SoilFertilizerSerializer(soil_fertilizer)
        except SoilFertilizer.DoesNotExist as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        soil_fertilizer = get_object_or_404(SoilFertilizer, pk=pk)
        soil_analysis = get_object_or_404(
            SoilFertilizer, pk=soil_fertilizer.soil_analysis.id
        )
        weather_conditions = get_object_or_404(
            SoilFertilizer, pk=soil_fertilizer.weather_conditions.id
        )
        try:
            with transaction.atomic():
                soil_fertilizer.delete()
                soil_analysis.delete()
                weather_conditions.delete()
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {"message": "Soil fertilizer deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
