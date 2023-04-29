from django.urls import path

from .views import PlantDiseaseList, PlantDiseasePost, PlantDiseaseRetrieveDestroy

urlpatterns = [
    path("predict/", PlantDiseasePost.as_view(), name="plant-disease"),
    path("list/", PlantDiseaseList.as_view(), name="list-diseases"),
    path(
        "details/<int:id>/",
        PlantDiseaseRetrieveDestroy.as_view(),
        name="plant-disease-destroy",
    ),
]
