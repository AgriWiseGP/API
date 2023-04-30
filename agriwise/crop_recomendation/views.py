from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from agriwise.core.permissions import IsOwnerOrReadOnly
from agriwise.users.models import User

from .ml_models.crop_recommendation import RandomForestClassifier
from .models import CropRecommendation
from .serializers import CropRecommendationSerializer, SoilElementsSerializer


class CropRecommendationPostListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        soil_serializer = SoilElementsSerializer(data=request.data)
        if soil_serializer.is_valid():
            soil_element = soil_serializer.save()

            # Run the ML model on the input data
            clf = RandomForestClassifier()
            prediction = clf.compute_prediction(
                [
                    [
                        soil_element.n,
                        soil_element.p,
                        soil_element.k,
                        soil_element.temperature,
                        soil_element.humidity,
                        soil_element.ph,
                        soil_element.rainfall,
                    ]
                ]
            )

            #  crop_serializer for serialization of the CropRecommendation data
            crop_serializer = CropRecommendationSerializer(
                data={
                    "name": prediction,
                    "user": request.user.id,
                    "soil_elements": soil_element.id,
                }
            )

            if crop_serializer.is_valid():
                # Save the CropRecommendation data to the db
                crop_serializer.save()

                # Return a success response with the created CropRecommendation data
                return Response(
                    {
                        "message": "Crop recommendation saved successfully",
                        "data": crop_serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                # If the CropRecommendation data is invalid Delete the SoilElement data
                soil_element.delete()
                return Response(
                    {
                        "message": "Invalid crop recommendation data",
                        "errors": crop_serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Return error if the soil data is invalid
        else:
            return Response(
                {
                    "message": "Invalid soil element data",
                    "errors": soil_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    # may be helpful for adminstrators

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            crops = CropRecommendation.objects.all()
            crop_serializer = CropRecommendationSerializer(crops, many=True)
            return Response(crop_serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "You are not allowed"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class CropsGetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        crops = CropRecommendation.objects.filter(user=user)
        crop_serializer = CropRecommendationSerializer(crops, many=True)
        return Response(crop_serializer.data, status=status.HTTP_200_OK)


class CropGetDeleteApi(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, username, crop_id, *args, **kwargs):
        try:
            crop = CropRecommendation.objects.select_related("soil_elements").get(
                id=crop_id, user__username=username
            )
            crop_serializer = CropRecommendationSerializer(crop)
        except CropRecommendation.DoesNotExist as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(crop_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, username, crop_id, *args, **kwargs):
        crop = get_object_or_404(
            CropRecommendation, id=crop_id, user__username=username
        )
        try:
            with transaction.atomic():
                soil_elements = crop.soil_elements
                crop.delete()
                soil_elements.delete()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {"message": "Crop recommendation instance deleted successfully."},
            status=status.HTTP_200_OK,
        )
