import pytest
from datetime import datetime
from uuid import UUID

from src.models.todo import Todo


def test_todo_creation():
    """Test creating a valid Todo."""
    todo = Todo(title="Test task", description="Test description")

    assert todo.title == "Test task"
    assert todo.description == "Test description"
    assert not todo.completed
    assert isinstance(todo.id, UUID)
    assert isinstance(todo.created_at, datetime)
    assert isinstance(todo.updated_at, datetime)


def test_todo_creation_defaults():
    """Test Todo creation with default values."""
    todo = Todo(title="Test task")

    assert todo.title == "Test task"
    assert todo.description == ""
    assert not todo.completed


def test_todo_mark_complete():
    """Test marking a todo as complete."""
    todo = Todo(title="Test task")

    assert not todo.completed
    todo.mark_complete()
    assert todo.completed
    assert isinstance(todo.updated_at, datetime)


def test_todo_mark_incomplete():
    """Test marking a todo as incomplete."""
    todo = Todo(title="Test task")
    todo.mark_complete()

    assert todo.completed
    todo.mark_incomplete()
    assert not todo.completed
    assert isinstance(todo.updated_at, datetime)


def test_todo_update():
    """Test updating a todo."""
    todo = Todo(title="Test task", description="Original description")
    original_updated_at = todo.updated_at

    todo.update(title="Updated task", description="Updated description")

    assert todo.title == "Updated task"
    assert todo.description == "Updated description"
    assert todo.updated_at > original_updated_at


def test_todo_update_partial():
    """Test updating only title or description."""
    todo = Todo(title="Test task", description="Test description")

    # Update only title
    original_desc = todo.description
    todo.update(title="Updated task")
    assert todo.title == "Updated task"
    assert todo.description == original_desc

    # Update only description
    original_title = todo.title
    original_updated_at = todo.updated_at
    todo.update(description="New description")
    assert todo.title == original_title
    assert todo.description == "New description"
    assert todo.updated_at > original_updated_at


def test_title_validation_min_length():
    """Test title validation for minimum length."""
    with pytest.raises(ValueError, match="Title cannot be empty or whitespace only"):
        Todo(title="")


def test_title_validation_whitespace_only():
    """Test title validation for whitespace-only titles."""
    with pytest.raises(ValueError, match="Title cannot be empty or whitespace only"):
        Todo(title="   ")


def test_title_validation_max_length():
    """Test title validation for maximum length."""
    long_title = "a" * 201
    with pytest.raises(ValueError, match="Title must be 200 characters or less"):
        Todo(title=long_title)


def test_description_validation_max_length():
    """Test description validation for maximum length."""
    long_description = "a" * 1001
    with pytest.raises(ValueError, match="Description must be 1000 characters or less"):
        Todo(title="Test", description=long_description)


def test_title_stripping():
    """Test that title gets stripped of leading/trailing whitespace."""
    todo = Todo(title="  Test task  ")
    assert todo.title == "Test task"


def test_title_required():
    """Test that title is required."""
    with pytest.raises(ValueError):
        Todo(title=None)