from django.urls import path

from .views import SoilTypeList, SoilTypePost, SoilTypeRetrieveDestroy

urlpatterns = [
    path("predict/", SoilTypePost.as_view(), name="soil-type"),
    path("list/", SoilTypeList.as_view(), name="list-types"),
    path(
        "details/<int:id>/", SoilTypeRetrieveDestroy.as_view(), name="soiltype-destroy"
    ),
]
