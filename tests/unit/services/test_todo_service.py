import pytest
from datetime import datetime, timedelta
from src.services.todo_service import TodoService
from src.models.todo import Todo, TodoStatus


class TestTodoService:
    """Test cases for TodoService"""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.todo_service = TodoService()

    def test_create_todo(self):
        """Test creating a new todo."""
        title = "Test Todo"
        description = "Test Description"
        due_date = datetime.now() + timedelta(days=1)

        todo = self.todo_service.create_todo(title, description, due_date)

        assert todo.title == title
        assert todo.description == description
        assert todo.due_date == due_date
        assert todo.status == TodoStatus.PENDING
        assert todo.id == 1  # First todo should have ID 1

    def test_get_todo(self):
        """Test getting a todo by ID."""
        # Create a todo first
        created_todo = self.todo_service.create_todo("Test Todo")

        # Retrieve the todo
        retrieved_todo = self.todo_service.get_todo(created_todo.id)

        assert retrieved_todo is not None
        assert retrieved_todo.id == created_todo.id
        assert retrieved_todo.title == created_todo.title

    def test_get_todo_not_found(self):
        """Test getting a non-existent todo."""
        todo = self.todo_service.get_todo(999)

        assert todo is None

    def test_get_all_todos(self):
        """Test getting all todos."""
        # Create multiple todos
        todo1 = self.todo_service.create_todo("Todo 1")
        todo2 = self.todo_service.create_todo("Todo 2")

        all_todos = self.todo_service.get_all_todos()

        assert len(all_todos) == 2
        assert todo1 in all_todos
        assert todo2 in all_todos

    def test_get_todos_by_status(self):
        """Test getting todos by status."""
        # Create todos with different statuses
        todo1 = self.todo_service.create_todo("Todo 1")
        todo2 = self.todo_service.create_todo("Todo 2")

        # Mark one as completed
        self.todo_service.mark_todo_completed(todo2.id)

        pending_todos = self.todo_service.get_todos_by_status(TodoStatus.PENDING)
        completed_todos = self.todo_service.get_todos_by_status(TodoStatus.COMPLETED)

        assert len(pending_todos) == 1
        assert len(completed_todos) == 1
        assert pending_todos[0].id == todo1.id
        assert completed_todos[0].id == todo2.id

    def test_update_todo(self):
        """Test updating a todo."""
        # Create a todo
        original_todo = self.todo_service.create_todo("Original Title", "Original Description")

        # Update the todo
        updated_title = "Updated Title"
        updated_description = "Updated Description"
        updated_todo = self.todo_service.update_todo(
            original_todo.id,
            title=updated_title,
            description=updated_description
        )

        assert updated_todo is not None
        assert updated_todo.title == updated_title
        assert updated_todo.description == updated_description

    def test_delete_todo(self):
        """Test deleting a todo."""
        # Create a todo
        todo = self.todo_service.create_todo("Test Todo")

        # Delete the todo
        success = self.todo_service.delete_todo(todo.id)

        assert success is True
        assert self.todo_service.get_todo(todo.id) is None

    def test_delete_todo_not_found(self):
        """Test deleting a non-existent todo."""
        success = self.todo_service.delete_todo(999)

        assert success is False

    def test_mark_todo_completed(self):
        """Test marking a todo as completed."""
        todo = self.todo_service.create_todo("Test Todo")

        completed_todo = self.todo_service.mark_todo_completed(todo.id)

        assert completed_todo is not None
        assert completed_todo.status == TodoStatus.COMPLETED

    def test_mark_todo_in_progress(self):
        """Test marking a todo as in progress."""
        todo = self.todo_service.create_todo("Test Todo")

        in_progress_todo = self.todo_service.mark_todo_in_progress(todo.id)

        assert in_progress_todo is not None
        assert in_progress_todo.status == TodoStatus.IN_PROGRESS

    def test_mark_todo_pending(self):
        """Test marking a todo as pending."""
        todo = self.todo_service.create_todo("Test Todo")
        # First mark as completed
        self.todo_service.mark_todo_completed(todo.id)

        # Then mark as pending
        pending_todo = self.todo_service.mark_todo_pending(todo.id)

        assert pending_todo is not None
        assert pending_todo.status == TodoStatus.PENDING