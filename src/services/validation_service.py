from typing import Any, Dict, List, Optional
from pydantic import ValidationError
from src.models.todo import Todo
from src.models.user import User


class ValidationService:
    """
    Service for validating input data and business rules.
    """

    @staticmethod
    def validate_todo_data(data: Dict[str, Any]) -> Optional[str]:
        """
        Validate todo data and return error message if invalid, None if valid.
        """
        try:
            # Try to create a Todo object to validate the data
            Todo(**data)
            return None
        except ValidationError as e:
            return str(e)

    @staticmethod
    def validate_user_data(data: Dict[str, Any]) -> Optional[str]:
        """
        Validate user data and return error message if invalid, None if valid.
        """
        try:
            # Try to create a User object to validate the data
            User(**data)
            return None
        except ValidationError as e:
            return str(e)

    @staticmethod
    def validate_todo_title(title: str) -> List[str]:
        """
        Validate todo title and return list of validation errors.
        """
        errors = []

        if not title or len(title.strip()) == 0:
            errors.append("Title cannot be empty")
        elif len(title) > 200:
            errors.append("Title cannot exceed 200 characters")

        return errors

    @staticmethod
    def validate_todo_description(description: Optional[str]) -> List[str]:
        """
        Validate todo description and return list of validation errors.
        """
        errors = []

        if description and len(description) > 1000:
            errors.append("Description cannot exceed 1000 characters")

        return errors

    @staticmethod
    def validate_username(username: str) -> List[str]:
        """
        Validate username and return list of validation errors.
        """
        errors = []

        if not username or len(username.strip()) == 0:
            errors.append("Username cannot be empty")
        elif len(username) < 3:
            errors.append("Username must be at least 3 characters long")
        elif len(username) > 50:
            errors.append("Username cannot exceed 50 characters")
        elif not username.replace('_', '').replace('-', '').isalnum():
            errors.append("Username can only contain letters, numbers, underscores, and hyphens")

        return errors

    @staticmethod
    def validate_email(email: str) -> List[str]:
        """
        Validate email address and return list of validation errors.
        """
        import re

        errors = []

        if not email or len(email.strip()) == 0:
            errors.append("Email cannot be empty")
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append("Invalid email format")

        return errors

    @staticmethod
    def validate_password(password: str) -> List[str]:
        """
        Validate password and return list of validation errors.
        """
        errors = []

        if not password or len(password) < 8:
            errors.append("Password must be at least 8 characters long")

        return errors