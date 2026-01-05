from typing import Dict, List, Optional
from uuid import UUID

from src.models.todo import Todo


class InMemoryTodoStorage:
    """
    In-memory storage for todos.
    """
    def __init__(self) -> None:
        self._todos: Dict[UUID, Todo] = {}

    def add_todo(self, todo: Todo) -> Todo:
        """Add a todo to storage."""
        self._todos[todo.id] = todo
        return todo

    def get_todo(self, todo_id: UUID) -> Optional[Todo]:
        """Get a todo by ID."""
        return self._todos.get(todo_id)

    def get_all_todos(self) -> List[Todo]:
        """Get all todos."""
        return list(self._todos.values())

    def update_todo(self, todo_id: UUID, todo: Todo) -> Optional[Todo]:
        """Update a todo in storage."""
        if todo_id in self._todos:
            self._todos[todo_id] = todo
            return todo
        return None

    def delete_todo(self, todo_id: UUID) -> bool:
        """Delete a todo from storage."""
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False

    def clear_all(self) -> None:
        """Clear all todos from storage (for testing purposes)."""
        self._todos.clear()