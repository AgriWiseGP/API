from django.urls import path

from agriwise.users.api.views import (
    PasswordChangeView,
    UserDetailsForOtherUsersView,
    UserDetailsView,
    UsersListView,
)

urlpatterns = [
    path("", UsersListView.as_view(), name="list-all-users"),
    path("<uuid:pk>", UserDetailsForOtherUsersView.as_view(), name="user-details"),
    path("me/", UserDetailsView.as_view(), name="current-user-details"),
    path("me/password-change/", PasswordChangeView.as_view(), name="password-change"),
]
