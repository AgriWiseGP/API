from django.urls import path
from .views import SoilQualityPostList, SoilQualityDetailsAPIView

urlpatterns = [

    path(
        "soil/",
        SoilQualityPostList.as_view(),
        name="soil_quality_post_list",
    ),
    path("soil/<int:pk>", SoilQualityDetailsAPIView.as_view()),

]