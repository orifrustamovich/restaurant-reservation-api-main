import pytest
from rest_framework.test import APIClient
from tests.factories import UserFactory, OwnerFactory, RestaurantFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def customer(db):
    return UserFactory()


@pytest.fixture
def owner(db):
    return OwnerFactory()


@pytest.fixture
def restaurant(db):
    return RestaurantFactory()


@pytest.fixture
def auth_client(api_client, customer):
    """Customer sifatida autentifikatsiya qilingan client"""
    api_client.force_authenticate(user=customer)
    return api_client


@pytest.fixture
def owner_client(api_client, owner):
    """Owner sifatida autentifikatsiya qilingan client"""
    api_client.force_authenticate(user=owner)
    return api_client