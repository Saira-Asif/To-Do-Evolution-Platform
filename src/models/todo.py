from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class Todo(BaseModel):
    """
    Todo data model with validation rules.
    """
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: Optional[str] = Field(default="")
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate that title is not empty or whitespace only and is not too long."""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        if len(v) > 200:
            raise ValueError('Title must be 200 characters or less')
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validate that description is not too long."""
        if v is None:
            return v
        if len(v) > 1000:
            raise ValueError('Description must be 1000 characters or less')
        return v

    def mark_complete(self) -> None:
        """Mark the todo as complete and update the timestamp."""
        self.completed = True
        self.updated_at = datetime.now()

    def mark_incomplete(self) -> None:
        """Mark the todo as incomplete and update the timestamp."""
        self.completed = False
        self.updated_at = datetime.now()

    def update(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """Update the todo with new values and update the timestamp."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()