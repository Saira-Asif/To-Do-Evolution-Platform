from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """
    Base model for User with common fields.
    """
    email: str = Field(unique=True, nullable=False)
    name: Optional[str] = Field(default=None, max_length=100)


class User(UserBase, table=True):
    """
    User model for the Todo Web Application.
    Managed primarily by Better Auth, but defined here for integration purposes.
    """
    id: str = Field(primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    """
    Model for creating new users.
    """
    password: str
    name: Optional[str] = Field(default=None, max_length=100)


class TaskBase(SQLModel):
    """
    Base model for Task with common fields.
    """
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """
    Task model for the Todo Web Application.
    Represents individual todo items owned by a user.
    """
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(TaskBase):
    """
    Model for creating new tasks.
    """
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class TaskUpdate(SQLModel):
    """
    Model for updating existing tasks.
    All fields are optional to allow partial updates.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)


class TaskPublic(TaskBase):
    """
    Public model for returning task data via API.
    Includes ID and timestamps but excludes user_id for security.
    """
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime