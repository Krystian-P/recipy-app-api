"""
Test for Django admin modifications.
"""
from django.contrib.auth import get_user_model
from django.template.response import TemplateResponse
from django.test import Client
from django.urls import reverse
from pytest import mark, fixture


@mark.django_db
class TestAdminSite:
    """Tests for django admin."""

    @fixture
    def user(self):
        return get_user_model().objects.create_user(
            email='user@example.com',
            password='1234',
            name='Test User'
        )

    @fixture
    def client(self, user) -> Client:
        client = Client()
        admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='1234'
        )
        client.force_login(admin_user)
        return client

    def test_user_list(self, client: Client, user) -> None:
        """Tests that users are listed on page."""
        url = reverse('admin:core_user_changelist')
        res: TemplateResponse = client.get(url)
        assert user.name in str(res.content)
        assert user.email in str(res.content)

    def test_edit_user_page(self, client: Client, user) -> None:
        """Test the edit user page works."""
        url = reverse('admin:core_user_change', args=[user.id])
        res = client.get(url)
        assert res.status_code == 200

    def test_create_user_page(self, client: Client, user) -> None:
        """Test the create user page works"""
        url = reverse('admin:core_user_add')
        res = client.get(url)
        assert res.status_code == 200