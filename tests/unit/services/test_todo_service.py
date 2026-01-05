from uuid import UUID

import pytest

from src.models.storage import InMemoryTodoStorage
from src.models.todo import Todo
from src.services.todo_service import TodoService


class TestTodoService:
    def setup_method(self):
        """Set up a fresh service instance for each test."""
        self.storage = InMemoryTodoStorage()
        self.service = TodoService(self.storage)

    def test_add_task(self):
        """Test adding a task."""
        title = "Test task"
        description = "Test description"

        todo = self.service.add_task(title, description)

        assert todo.title == title
        assert todo.description == description
        assert not todo.completed
        assert isinstance(todo.id, UUID)

    def test_add_task_without_description(self):
        """Test adding a task without description."""
        title = "Test task"

        todo = self.service.add_task(title)

        assert todo.title == title
        assert todo.description == ""
        assert not todo.completed

    def test_add_task_validation_error(self):
        """Test that validation errors are propagated."""
        long_title = "a" * 201

        with pytest.raises(ValueError):
            self.service.add_task(long_title)

    def test_get_all_tasks_empty(self):
        """Test getting all tasks when none exist."""
        todos = self.service.get_all_tasks()

        assert len(todos) == 0

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        todo1 = self.service.add_task("Task 1", "Description 1")
        todo2 = self.service.add_task("Task 2", "Description 2")

        todos = self.service.get_all_tasks()

        assert len(todos) == 2
        assert todo1 in todos
        assert todo2 in todos

    def test_update_task(self):
        """Test updating a task."""
        original_todo = self.service.add_task("Original task", "Original description")
        new_title = "Updated task"
        new_description = "Updated description"

        updated_todo = self.service.update_task(original_todo.id, new_title, new_description)

        assert updated_todo is not None
        assert updated_todo.title == new_title
        assert updated_todo.description == new_description

    def test_update_task_partial(self):
        """Test updating only title or description."""
        original_todo = self.service.add_task("Original task", "Original description")

        # Update only title
        updated_todo = self.service.update_task(original_todo.id, title="Updated title")
        assert updated_todo.title == "Updated title"
        assert updated_todo.description == "Original description"

        # Update only description
        updated_todo = self.service.update_task(original_todo.id, description="Updated description")
        assert updated_todo.title == "Updated title"
        assert updated_todo.description == "Updated description"

    def test_update_task_not_found(self):
        """Test updating a non-existent task."""
        fake_id = UUID("12345678-1234-5678-1234-567812345678")

        result = self.service.update_task(fake_id, "New title")

        assert result is None

    def test_update_task_validation_error(self):
        """Test that validation errors are propagated during update."""
        original_todo = self.service.add_task("Original task")

        with pytest.raises(ValueError):
            self.service.update_task(original_todo.id, "a" * 201)  # Too long title

    def test_delete_task(self):
        """Test deleting a task."""
        todo = self.service.add_task("Test task")

        result = self.service.delete_task(todo.id)

        assert result is True
        assert len(self.service.get_all_tasks()) == 0

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        fake_id = UUID("12345678-1234-5678-1234-567812345678")

        result = self.service.delete_task(fake_id)

        assert result is False

    def test_complete_task(self):
        """Test marking a task as complete."""
        todo = self.service.add_task("Test task")
        assert not todo.completed

        completed_todo = self.service.complete_task(todo.id)

        assert completed_todo is not None
        assert completed_todo.completed

    def test_complete_task_not_found(self):
        """Test completing a non-existent task."""
        fake_id = UUID("12345678-1234-5678-1234-567812345678")

        result = self.service.complete_task(fake_id)

        assert result is None

    def test_uncomplete_task(self):
        """Test marking a task as incomplete."""
        todo = self.service.add_task("Test task")
        completed_todo = self.service.complete_task(todo.id)
        assert completed_todo.completed

        uncompleted_todo = self.service.uncomplete_task(todo.id)

        assert uncompleted_todo is not None
        assert not uncompleted_todo.completed

    def test_uncomplete_task_not_found(self):
        """Test uncompleting a non-existent task."""
        fake_id = UUID("12345678-1234-5678-1234-567812345678")

        result = self.service.uncomplete_task(fake_id)

        assert result is None