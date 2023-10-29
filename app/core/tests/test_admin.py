"""
Test for Django admin modifications.
"""
from django.template.response import TemplateResponse
from pytest import mark, fixture
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


@mark.django_db
class TestAdminSite:
    """Tests for django admin."""

    @fixture
    def client(self):
        client = Client()
        admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='1234'
        )
        client.force_login(admin_user)
        return client

    def test_user_list(self, client):
        """Tests that users are listed on page."""
        user = get_user_model().objects.create_user(
            email='user@example.com',
            password='1234',
            name='Test User'
        )

        url = reverse('admin:core_user_changelist')
        res: TemplateResponse = client.get(url)
        assert user.name in str(res.content)
        assert user.email in str(res.content)
