import pytest
from datetime import datetime
from src.models.todo import Todo, TodoStatus


class TestTodo:
    """Test cases for Todo model"""

    def test_todo_creation(self):
        """Test creating a todo with all fields."""
        todo = Todo(
            title="Test Todo",
            description="Test Description",
            status=TodoStatus.PENDING,
            due_date=datetime.now()
        )

        assert todo.title == "Test Todo"
        assert todo.description == "Test Description"
        assert todo.status == TodoStatus.PENDING

    def test_todo_creation_optional_fields(self):
        """Test creating a todo with minimal fields."""
        todo = Todo(title="Test Todo")

        assert todo.title == "Test Todo"
        assert todo.description is None
        assert todo.status == TodoStatus.PENDING
        assert todo.due_date is None

    def test_mark_completed(self):
        """Test marking a todo as completed."""
        todo = Todo(title="Test Todo")

        todo.mark_completed()

        assert todo.status == TodoStatus.COMPLETED

    def test_mark_in_progress(self):
        """Test marking a todo as in progress."""
        todo = Todo(title="Test Todo")

        todo.mark_in_progress()

        assert todo.status == TodoStatus.IN_PROGRESS

    def test_mark_pending(self):
        """Test marking a todo as pending."""
        todo = Todo(title="Test Todo", status=TodoStatus.COMPLETED)

        todo.mark_pending()

        assert todo.status == TodoStatus.PENDING

    def test_todo_validation_title_too_long(self):
        """Test validation for title that's too long."""
        with pytest.raises(ValueError):
            Todo(title="A" * 201)  # More than 200 characters

    def test_todo_validation_description_too_long(self):
        """Test validation for description that's too long."""
        with pytest.raises(ValueError):
            Todo(title="Test", description="A" * 1001)  # More than 1000 characters