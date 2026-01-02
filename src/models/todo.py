from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class TodoStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Todo(BaseModel):
    """
    Todo data model representing a todo item with title, description, status, and due date.
    """
    id: Optional[int] = Field(default=None, description="Unique identifier for the todo")
    title: str = Field(..., min_length=1, max_length=200, description="Title of the todo")
    description: Optional[str] = Field(default=None, max_length=1000, description="Detailed description of the todo")
    status: TodoStatus = Field(default=TodoStatus.PENDING, description="Current status of the todo")
    due_date: Optional[datetime] = Field(default=None, description="Due date for the todo")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when todo was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="Timestamp when todo was last updated")

    def mark_completed(self):
        """Mark the todo as completed"""
        self.status = TodoStatus.COMPLETED
        self.updated_at = datetime.now()

    def mark_in_progress(self):
        """Mark the todo as in progress"""
        self.status = TodoStatus.IN_PROGRESS
        self.updated_at = datetime.now()

    def mark_pending(self):
        """Mark the todo as pending"""
        self.status = TodoStatus.PENDING
        self.updated_at = datetime.now()

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }