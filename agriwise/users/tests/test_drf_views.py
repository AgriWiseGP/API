import pytest
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import RequestFactory
from djoser.utils import encode_uid
from rest_framework.test import APIClient

from agriwise.users.api.views import UserViewSet
from agriwise.users.models import User

token_generator = PasswordResetTokenGenerator()
client = APIClient()


class TestUserViewSet:
    def test_get_queryset(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)

        assert response.data == {
            "username": user.username,
            "name": user.name,
            "url": f"http://testserver/api/users/{user.username}/",
        }


@pytest.mark.django_db
class TestActivationEmail:
    def test_successfull_account_activation_authorized_user(self, auth_client, user):
        uid = encode_uid(user.pk)
        user_token = token_generator.make_token(user)
        response = auth_client.get(
            "/users/auth/api/users/activation/" + str(uid) + "/" + str(user_token)
        )
        assert response.status_code == 200
        # hard refresh the object from db
        user = User.objects.get(id=user.id)
        assert user.is_verified

    def test_successfull_account_activation_unauthorized_user(self, client, user):
        uid = encode_uid(user.pk)
        user_token = token_generator.make_token(user)
        response = client.get(
            "/users/auth/api/users/activation/" + uid + "/" + user_token
        )
        assert response.status_code == 200
        # hard refresh the object from db
        user = User.objects.get(id=user.id)
        assert user.is_verified

    def test_account_activation_for_already_activated_account(self, client, user):
        # set is_verified to true to indicate activated account
        User.objects.filter(id=user.pk).update(is_verified=True)
        # hard refresh the object from db
        user = User.objects.get(id=user.id)
        uid = encode_uid(user.pk)
        user_token = token_generator.make_token(user)
        response = client.get(
            "/users/auth/api/users/activation/" + uid + "/" + user_token
        )
        assert response.status_code == 400
