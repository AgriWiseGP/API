from django.urls import path

from agriwise.agriculture_specialist.views import (
    AgricultureSpecialistDetailView,
    AgricultureSpecialistView,
    ProfileUpgradeUserDetailsView,
    ProfileUpgradeUserView,
)

urlpatterns = [
    path("", ProfileUpgradeUserView.as_view()),
    path("<int:pk>", ProfileUpgradeUserDetailsView.as_view()),
    path("specialists/", AgricultureSpecialistView.as_view()),
    path("specialists/<uuid:pk>", AgricultureSpecialistDetailView.as_view()),
]
