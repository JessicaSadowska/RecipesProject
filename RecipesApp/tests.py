from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
import pytest


@pytest.fixture
def user():
    user = User.objects.create(
        username="testuser",
        first_name="Jan",
        last_name="Nowak",
        email="test@test.com",
        password="test123"
    )
    return user


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.mark.django_db
def test_test(client):
    response = client.get('')
    assert response.status_code == 200



