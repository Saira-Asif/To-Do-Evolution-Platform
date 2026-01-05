from typing import List, Optional
from uuid import UUID

from src.models.storage import InMemoryTodoStorage
from src.models.todo import Todo


class TodoService:
    """
    Service layer for todo operations.
    """
    def __init__(self, storage: InMemoryTodoStorage) -> None:
        self.storage = storage

    def add_task(self, title: str, description: Optional[str] = None) -> Todo:
        """
        Add a new task.

        Args:
            title: The task title (1-200 characters)
            description: Optional task description (max 1000 characters)

        Returns:
            The created Todo object

        Raises:
            ValueError: If title or description validation fails
        """
        # Create a new Todo instance
        todo = Todo(title=title, description=description or "")
        # Add to storage and return
        return self.storage.add_todo(todo)

    def get_all_tasks(self) -> List[Todo]:
        """
        Get all tasks.

        Returns:
            List of all Todo objects
        """
        return self.storage.get_all_todos()

    def update_task(self, todo_id: UUID, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Todo]:
        """
        Update an existing task.

        Args:
            todo_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            The updated Todo object, or None if not found

        Raises:
            ValueError: If title or description validation fails
        """
        existing_todo = self.storage.get_todo(todo_id)
        if existing_todo is None:
            return None

        # Update the todo with provided values
        if title is not None:
            # Create a temporary Todo to validate the new title
            Todo(title=title, description=existing_todo.description)
            existing_todo.title = title
        if description is not None:
            # Create a temporary Todo to validate the new description
            Todo(title=existing_todo.title, description=description)
            existing_todo.description = description
        existing_todo.updated_at = existing_todo.updated_at  # This will update the timestamp

        # Save the updated todo
        return self.storage.update_todo(todo_id, existing_todo)

    def delete_task(self, todo_id: UUID) -> bool:
        """
        Delete a task by ID.

        Args:
            todo_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if not found
        """
        return self.storage.delete_todo(todo_id)

    def complete_task(self, todo_id: UUID) -> Optional[Todo]:
        """
        Mark a task as complete.

        Args:
            todo_id: The ID of the task to mark as complete

        Returns:
            The updated Todo object, or None if not found
        """
        existing_todo = self.storage.get_todo(todo_id)
        if existing_todo is None:
            return None

        existing_todo.mark_complete()
        return self.storage.update_todo(todo_id, existing_todo)

    def uncomplete_task(self, todo_id: UUID) -> Optional[Todo]:
        """
        Mark a task as incomplete.

        Args:
            todo_id: The ID of the task to mark as incomplete

        Returns:
            The updated Todo object, or None if not found
        """
        existing_todo = self.storage.get_todo(todo_id)
        if existing_todo is None:
            return None

        existing_todo.mark_incomplete()
        return self.storage.update_todo(todo_id, existing_todo)