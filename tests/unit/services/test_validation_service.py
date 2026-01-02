import pytest
from datetime import datetime
from src.services.validation_service import ValidationService
from src.models.todo import TodoStatus


class TestValidationService:
    """Test cases for ValidationService"""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.validation_service = ValidationService()

    def test_validate_todo_data_valid(self):
        """Test validating valid todo data."""
        valid_data = {
            "title": "Valid Todo",
            "description": "Valid Description",
            "status": TodoStatus.PENDING,
            "due_date": datetime.now()
        }

        error = self.validation_service.validate_todo_data(valid_data)

        assert error is None

    def test_validate_todo_data_invalid_title(self):
        """Test validating todo data with invalid title."""
        invalid_data = {
            "title": "",  # Empty title should be invalid
            "description": "Valid Description"
        }

        error = self.validation_service.validate_todo_data(invalid_data)

        assert error is not None
        assert "title" in error.lower()

    def test_validate_user_data_valid(self):
        """Test validating valid user data."""
        valid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": "hashed_password_123"
        }

        error = self.validation_service.validate_user_data(valid_data)

        assert error is None

    def test_validate_user_data_invalid_email(self):
        """Test validating user data with invalid email."""
        invalid_data = {
            "username": "testuser",
            "email": "invalid_email",  # Invalid email format
            "password_hash": "hashed_password_123"
        }

        error = self.validation_service.validate_user_data(invalid_data)

        assert error is not None
        assert "email" in error.lower()

    def test_validate_todo_title_valid(self):
        """Test validating a valid todo title."""
        errors = self.validation_service.validate_todo_title("Valid Title")

        assert len(errors) == 0

    def test_validate_todo_title_empty(self):
        """Test validating an empty todo title."""
        errors = self.validation_service.validate_todo_title("")

        assert len(errors) == 1
        assert "cannot be empty" in errors[0]

    def test_validate_todo_title_too_long(self):
        """Test validating a todo title that's too long."""
        long_title = "A" * 201  # More than 200 characters
        errors = self.validation_service.validate_todo_title(long_title)

        assert len(errors) == 1
        assert "cannot exceed" in errors[0]

    def test_validate_todo_description_valid(self):
        """Test validating a valid todo description."""
        errors = self.validation_service.validate_todo_description("Valid description")

        assert len(errors) == 0

    def test_validate_todo_description_too_long(self):
        """Test validating a todo description that's too long."""
        long_description = "A" * 1001  # More than 1000 characters
        errors = self.validation_service.validate_todo_description(long_description)

        assert len(errors) == 1
        assert "cannot exceed" in errors[0]

    def test_validate_username_valid(self):
        """Test validating a valid username."""
        errors = self.validation_service.validate_username("valid_user")

        assert len(errors) == 0

    def test_validate_username_too_short(self):
        """Test validating a username that's too short."""
        errors = self.validation_service.validate_username("ab")  # Less than 3 chars

        assert len(errors) == 1
        assert "at least 3 characters" in errors[0]

    def test_validate_username_invalid_characters(self):
        """Test validating a username with invalid characters."""
        errors = self.validation_service.validate_username("invalid@user")  # Contains @

        assert len(errors) == 1
        assert "can only contain" in errors[0]

    def test_validate_email_valid(self):
        """Test validating a valid email."""
        errors = self.validation_service.validate_email("test@example.com")

        assert len(errors) == 0

    def test_validate_email_invalid(self):
        """Test validating an invalid email."""
        errors = self.validation_service.validate_email("invalid_email")

        assert len(errors) == 1
        assert "Invalid email format" in errors[0]

    def test_validate_password_valid(self):
        """Test validating a valid password."""
        errors = self.validation_service.validate_password("validpassword")

        assert len(errors) == 0

    def test_validate_password_too_short(self):
        """Test validating a password that's too short."""
        errors = self.validation_service.validate_password("short")  # Less than 8 chars

        assert len(errors) == 1
        assert "at least 8 characters" in errors[0]