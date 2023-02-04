from django.urls import include, path
from djoser.views import UserViewSet

app_name = "users"
urlpatterns = [
    path("auth/api/", include("djoser.urls")),
    path("auth/api/", include("djoser.urls.jwt")),
    path("auth/api/users/activation/<str:uid>/<str:token>", UserViewSet().activation),
]
