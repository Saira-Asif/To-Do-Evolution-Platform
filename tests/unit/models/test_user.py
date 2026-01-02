import pytest
from datetime import datetime
from src.models.user import User, UserRole


class TestUser:
    """Test cases for User model"""

    def test_user_creation(self):
        """Test creating a user with all fields."""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password_123"
        )

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password_hash == "hashed_password_123"
        assert user.role == UserRole.USER  # Default role

    def test_user_creation_optional_fields(self):
        """Test creating a user with minimal fields."""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password_123"
        )

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password_hash == "hashed_password_123"
        assert user.is_active is True  # Default value
        assert user.is_verified is False  # Default value

    def test_user_deactivate(self):
        """Test deactivating a user account."""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password_123"
        )

        user.deactivate()

        assert user.is_active is False

    def test_user_activate(self):
        """Test activating a user account."""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password_123"
        )
        user.deactivate()  # First deactivate

        user.activate()

        assert user.is_active is True

    def test_user_verify_email(self):
        """Test verifying user's email."""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password_123"
        )

        user.verify_email()

        assert user.is_verified is True

    def test_user_update_last_login(self):
        """Test updating last login timestamp."""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password_123"
        )

        # Initially last_login should be None
        assert user.last_login is None

        # Update the last login
        user.update_last_login()

        # Now it should not be None
        assert user.last_login is not None

    def test_user_set_refresh_token(self):
        """Test setting refresh token."""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password_123"
        )

        user.set_refresh_token("token_hash")

        assert user.hashed_refresh_token == "token_hash"

    def test_user_clear_refresh_token(self):
        """Test clearing refresh token."""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password_123"
        )
        user.set_refresh_token("token_hash")

        user.clear_refresh_token()

        assert user.hashed_refresh_token is None

    def test_user_validation_invalid_email(self):
        """Test validation for invalid email format."""
        with pytest.raises(ValueError):
            User(username="testuser", email="invalid_email", password_hash="password")

    def test_user_validation_invalid_username(self):
        """Test validation for invalid username format."""
        with pytest.raises(ValueError):
            User(username="test@user", email="test@example.com", password_hash="password")

    def test_user_validation_username_too_short(self):
        """Test validation for username that's too short."""
        with pytest.raises(ValueError):
            User(username="ab", email="test@example.com", password_hash="password")