from django.urls import path

from agriwise.soil_fertilizer.views import (
    SoilFertilizerAPIView,
    SoilFertilizerDetailsAPIView,
)

urlpatterns = [
    path("", SoilFertilizerAPIView.as_view()),
    path("<int:pk>", SoilFertilizerDetailsAPIView.as_view()),
]
