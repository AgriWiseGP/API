from django.urls import path, include


app_name = "users"
urlpatterns = [
    path("auth/api/", include('djoser.urls')),
    path("auth/api/", include('djoser.urls.jwt')),
]