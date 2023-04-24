from django.urls import path

from agriwise.agriculture_specialist.views import (
    ProfileUpgradeUserDetailsView,
    ProfileUpgradeUserView,
)

urlpatterns = [
    path("", ProfileUpgradeUserView.as_view()),
    path("<int:pk>", ProfileUpgradeUserDetailsView.as_view()),
]
