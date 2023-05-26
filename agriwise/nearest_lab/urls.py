from django.urls import path

from .views import NurseryLocationList, SupplierLocationList

urlpatterns = [
    path(
        "supplier/",
        SupplierLocationList.as_view(),
        name="nearest_suppliers_list",
    ),
    path(
        "nursery/",
        NurseryLocationList.as_view(),
        name="nearest_nursery_list",
    ),
]
