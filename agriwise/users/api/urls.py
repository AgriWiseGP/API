from django.urls import include, path

app_name = "users"
urlpatterns = [
    path("auth/api/", include("djoser.urls")),
    path("auth/api/", include("djoser.urls.jwt")),
]
