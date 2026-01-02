from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, validator
import re


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class User(BaseModel):
    """
    User data model representing a user with authentication credentials.
    """
    id: Optional[int] = Field(default=None, description="Unique identifier for the user")
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: str = Field(..., description="User's email address")
    password_hash: str = Field(..., min_length=8, description="Hashed password for authentication")
    hashed_refresh_token: Optional[str] = Field(default=None, description="Hashed refresh token for authentication")
    role: UserRole = Field(default=UserRole.USER, description="User's role in the system")
    is_active: bool = Field(default=True, description="Whether the user account is active")
    is_verified: bool = Field(default=False, description="Whether the user email is verified")
    last_login: Optional[datetime] = Field(default=None, description="Timestamp of last login")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when user was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="Timestamp when user was last updated")

    @validator('email')
    def validate_email(cls, v):
        """Validate email format"""
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Invalid email format')
        return v.lower()

    @validator('username')
    def validate_username(cls, v):
        """Validate username format"""
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v.lower()

    def deactivate(self):
        """Deactivate the user account"""
        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self):
        """Activate the user account"""
        self.is_active = True
        self.updated_at = datetime.now()

    def verify_email(self):
        """Mark the user's email as verified"""
        self.is_verified = True
        self.updated_at = datetime.now()

    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = datetime.now()
        self.updated_at = datetime.now()

    def set_refresh_token(self, token_hash: str):
        """Set the refresh token hash"""
        self.hashed_refresh_token = token_hash
        self.updated_at = datetime.now()

    def clear_refresh_token(self):
        """Clear the refresh token"""
        self.hashed_refresh_token = None
        self.updated_at = datetime.now()

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }