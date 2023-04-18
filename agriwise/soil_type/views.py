from rest_framework import generics, permissions, status
from rest_framework.response import Response

from agriwise.soil_type.permissions import IsOwnerOrReadOnly
from agriwise.users.models import User

from .ml_models.soil_type import mobile_net
from .models import SoilType
from .serializers import SoilImageSerializer, SoilTypeSerializer


class SoilTypePost(generics.CreateAPIView):

    serializer_class = SoilImageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            uploaded_file = serializer.data["image"]
            uploaded_file_path = uploaded_file.lstrip("/")
            soil_type = mobile_net().compute_prediction(uploaded_file_path)
            soil_type_serializer = SoilTypeSerializer(data={"soil_type": soil_type})
            user = User.objects.filter(id=request.user.id).first()
            if soil_type_serializer.is_valid():
                soil_type_serializer.save(
                    soil_image=serializer.instance, user=user, soil_type=soil_type
                )
                return Response(
                    soil_type_serializer.data, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    soil_type_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SoilTypeList(generics.ListAPIView):
    serializer_class = SoilTypeSerializer
    queryset = SoilType.objects.select_related("soil_image").all()


class SoilTypeRetrieveDestroy(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = SoilTypeSerializer
    queryset = SoilType.objects.all()
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
