from django.urls import path

from .views import SoilQualityDetailsAPIView, SoilQualityPostList

urlpatterns = [
    path(
        "soil/",
        SoilQualityPostList.as_view(),
        name="soil_quality_post_list",
    ),
    path("soil/<int:pk>", SoilQualityDetailsAPIView.as_view()),
]
