from typing import List, Optional, Dict, Any
from datetime import datetime
from src.models.todo import Todo, TodoStatus
from src.services.validation_service import ValidationService


class TodoService:
    """
    Service for managing todo operations with in-memory storage.
    """

    def __init__(self):
        self.todos: List[Todo] = []
        self.next_id = 1
        self.validation_service = ValidationService()

    def create_todo(self, title: str, description: Optional[str] = None,
                   due_date: Optional[datetime] = None) -> Todo:
        """
        Create a new todo item.
        """
        # Validate the input data
        validation_errors = self.validation_service.validate_todo_title(title)
        if description:
            validation_errors.extend(self.validation_service.validate_todo_description(description))

        if validation_errors:
            raise ValueError(f"Validation failed: {'; '.join(validation_errors)}")

        # Create the new todo
        todo = Todo(
            id=self.next_id,
            title=title,
            description=description,
            due_date=due_date
        )

        self.todos.append(todo)
        self.next_id += 1

        return todo

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """
        Get a todo by its ID.
        """
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def get_all_todos(self, status: Optional[TodoStatus] = None) -> List[Todo]:
        """
        Get all todos, optionally filtered by status.
        """
        if status:
            return [todo for todo in self.todos if todo.status == status]
        return self.todos.copy()

    def update_todo(self, todo_id: int, **kwargs) -> Optional[Todo]:
        """
        Update a todo with the provided fields.
        """
        todo = self.get_todo(todo_id)
        if not todo:
            return None

        # Validate title if provided
        if 'title' in kwargs:
            validation_errors = self.validation_service.validate_todo_title(kwargs['title'])
            if validation_errors:
                raise ValueError(f"Validation failed: {'; '.join(validation_errors)}")

        # Validate description if provided
        if 'description' in kwargs:
            validation_errors = self.validation_service.validate_todo_description(kwargs['description'])
            if validation_errors:
                raise ValueError(f"Validation failed: {'; '.join(validation_errors)}")

        # Update the todo fields
        for key, value in kwargs.items():
            if hasattr(todo, key):
                setattr(todo, key, value)

        todo.updated_at = datetime.now()

        return todo

    def delete_todo(self, todo_id: int) -> bool:
        """
        Delete a todo by its ID.
        """
        original_length = len(self.todos)
        self.todos = [todo for todo in self.todos if todo.id != todo_id]
        return len(self.todos) < original_length

    def mark_todo_completed(self, todo_id: int) -> Optional[Todo]:
        """
        Mark a todo as completed.
        """
        todo = self.get_todo(todo_id)
        if todo:
            todo.mark_completed()
            return todo
        return None

    def mark_todo_in_progress(self, todo_id: int) -> Optional[Todo]:
        """
        Mark a todo as in progress.
        """
        todo = self.get_todo(todo_id)
        if todo:
            todo.mark_in_progress()
            return todo
        return None

    def mark_todo_pending(self, todo_id: int) -> Optional[Todo]:
        """
        Mark a todo as pending.
        """
        todo = self.get_todo(todo_id)
        if todo:
            todo.mark_pending()
            return todo
        return None

    def get_todos_by_status(self, status: TodoStatus) -> List[Todo]:
        """
        Get all todos with a specific status.
        """
        return [todo for todo in self.todos if todo.status == status]

    def get_overdue_todos(self) -> List[Todo]:
        """
        Get all overdue todos.
        """
        now = datetime.now()
        return [todo for todo in self.todos
                if todo.due_date and todo.due_date < now and todo.status != TodoStatus.COMPLETED]