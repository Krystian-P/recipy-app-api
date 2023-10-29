"""
Test for models.
"""
import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestModels:
    """Test models."""

    def test_create_user_with_email_successful(self) -> None:
        """Test creating a user with email is successful."""
        email = 'test@example.com'
        password = 'testpass1234'
        user = get_user_model().objects.create_user(
            email=email, password=password,
        )

        assert user.email == email
        assert user.check_password(password) is True

    @pytest.mark.parametrize("email, result", [
        ('test@example.com', 'test@example.com'),
        ('test@EXAMPLE.com', 'test@example.com'),
        ('Test@example.com', 'Test@example.com'),
        ('Test@EXAMPLE.com', 'Test@example.com'),
        ('test@EXAMPLE.COM', 'test@example.com'),
    ])
    def test_new_user_email_normalized(self, email: str, result: str) -> None:
        """Test email is normalized for new users."""
        user = get_user_model().objects.create_user(email, 'sample123')
        assert user.email == result

    def test_new_user_without_email_raise_error(self):
        """Test that creating new user without email raise error"""
        with pytest.raises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test that creating superusers"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        assert user.is_superuser is True
        assert user.is_staff is True
