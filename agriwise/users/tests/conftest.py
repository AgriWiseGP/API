import pytest
from rest_framework.test import APIClient

from agriwise.users.models import User


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(
        username="username1",
        email="username1@email.com",
        password="sh0123456789123456",
    )


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client
