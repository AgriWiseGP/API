from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction

from agriwise.users.models import User

from .ml_models.soil_quality import Soil_quality_Classifier
from agriwise.soil_quality.permissions import IsOwnerOrReadOnly
from .models import SoilQuality
from .serializers import SoilQualitySerializer, SoilAnalysisSerializer


class SoilQualityPostList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        soil_quality = SoilQuality.objects.select_related("soil_elements").filter(user=request.user)
        serializer = SoilQualitySerializer(soil_quality, many=True)
        return Response(serializer.data)

    def post(self, request):
        soil_elements_serializer = SoilAnalysisSerializer(data=request.data)
        if soil_elements_serializer.is_valid():
            soil_elements = soil_elements_serializer.save()

            clf = Soil_quality_Classifier()
            prediction = clf.compute_prediction(
                [
                    [
                        soil_elements.n,
                        soil_elements.p,
                        soil_elements.k,
                        soil_elements.ph,
                        soil_elements.ec,
                        soil_elements.oc,
                        soil_elements.s,
                        soil_elements.zn,
                        soil_elements.fe,
                        soil_elements.cu,
                        soil_elements.mu,
                        soil_elements.b,
                    ]
                ]
            )
            print("pridiction:", soil_elements.pk)
            print("soil elements", soil_elements)
            soil_quality_serializer = SoilQualitySerializer(
                data={
                    "quality": prediction,
                    "user": request.user.id,
                    "soil_elements": soil_elements_serializer.data,
                }
            )
            if soil_quality_serializer.is_valid():
                # Save the CropRecommendation data to the db
                soil_quality_serializer.save()

                # Return a success response with the created CropRecommendation data
                return Response(
                    {
                        "message": "soil quality saved successfully",
                        "data": soil_quality_serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                # If the soil quality data is invalid Delete the SoilElement data
                soil_quality_serializer.delete()
                return Response(
                    {
                        "message": "Invalid  soil quality data",
                        "errors": soil_quality_serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Return error if the soil data is invalid
        else:
            return Response(
                {
                    "message": "Invalid soil element data",
                    "errors": soil_elements_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class SoilQualityDetailsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, pk):
        try:
            soil_quality = SoilQuality.objects.select_related(
                "soil_elements").get(id=pk)
            serializer = SoilQualitySerializer(soil_quality)
        except SoilQuality.DoesNotExist as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        soil_quality = get_object_or_404(SoilQuality, id=pk)
        try:
            with transaction.atomic():
                soil_elements = soil_quality.soil_elements
                soil_quality.delete()
                soil_elements.delete()

        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {"message": "Soil quality instance deleted successfully."},
            status=status.HTTP_200_OK,
        )
