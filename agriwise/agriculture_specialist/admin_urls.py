from django.urls import path

from .views import ProfileUpgradeAdminDetailsView, ProfileUpgradeAdminView

urlpatterns = [
    path("all-pending-applications", ProfileUpgradeAdminView.as_view()),
    path("all-pending-applications/<int:pk>", ProfileUpgradeAdminDetailsView.as_view()),
]
