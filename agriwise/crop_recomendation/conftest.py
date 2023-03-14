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
def super_user(db) -> User:
    user= User.objects.create_superuser(
        username="username1",
        email="username1@email.com",
        password="sh0123456789123456",
    )
    user.is_superuser = True
    return user
     

@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture
def auth_client_super_user(super_user):
    client = APIClient()
    client.force_authenticate(super_user)
    return client

    