from django.urls import path

from .views import LocationList

urlpatterns = [
    path(
        "locations/",
        LocationList.as_view(),
        name="nearest_suppliers_list",
    ),
]
