import pytest
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from . import factories


@pytest.mark.django_db
class TestUsersView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_retrieve_user(self):
        user = factories.UserFactory.create()
        response = self.client.get(reverse('user_detail', args=[user.id]))
        user_from_response = response.context_data['user']
        self.assertTrue(response.status_code, 200)
        self.assertTrue(user_from_response.username, user.username)
        self.assertTrue(user_from_response.first_name, user.first_name)
        self.assertTrue(user_from_response.last_name, user.last_name)
        self.assertTrue(user_from_response.email, user.email)
