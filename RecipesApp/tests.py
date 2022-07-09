import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from RecipesApp import forms


@pytest.fixture
def user():
    user = User.objects.create(
        username="testuser",
        first_name="Jan",
        last_name="Nowak",
        email="test@test.com",
        password="test1234"
    )
    return user


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.mark.django_db
def test_MainPage(client):
    response = client.get('')
    assert response.status_code == 200


@pytest.mark.django_db
def test_Register(client):
    pass

class RegistrationTest(TestCase):

    def test_registration_view_get(self):
        """
        A ``GET`` to the ``register`` view uses the appropriate
        template and populates the registration form into the context.

        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'register.html')
        self.failUnless(isinstance(response.context['form'],
                                   forms.RegisterForm))


    def test_registration_view_post_success(self):
        """
        A ``POST`` to the ``register`` view with valid data properly
        creates a new user and issues a redirect.

        """
        response = self.client.post(reverse('register'),
                                    data={'username': 'testuser',
                                          'first_name': 'Jan',
                                          'last_name': 'Nowak',
                                          'email': 'test@test.com',
                                          'password': 'test1234',
                                          'password2': 'test1234'})
        self.assertRedirects(response, '/login/')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, 302)


class LoginLogoutTest(TestCase):

    def setUp(self):
        """
        NAPISZ
        """
        self.data = {
            'username': 'testuser',
            'password': 'test1234'}
        self.example_client = User.objects.create_user(**self.data)

    def test_login(self):
        """
        NAPISZ
        """
        response = self.client.post('/login/', self.data, follow=True)
        self.assertTrue(response.context['user'].is_active)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """
        NAPISZ
        """
        self.client.login(username='testuser', password="test1234")

        self.client.logout()
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)





