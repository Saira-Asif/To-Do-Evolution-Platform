from uuid import UUID

from src.models.storage import InMemoryTodoStorage
from src.models.todo import Todo


def test_add_todo():
    """Test adding a todo to storage."""
    storage = InMemoryTodoStorage()
    todo = Todo(title="Test task")

    added_todo = storage.add_todo(todo)

    assert added_todo.id == todo.id
    assert storage.get_todo(todo.id) == added_todo


def test_get_todo():
    """Test getting a todo by ID."""
    storage = InMemoryTodoStorage()
    todo = Todo(title="Test task")
    storage.add_todo(todo)

    retrieved_todo = storage.get_todo(todo.id)

    assert retrieved_todo is not None
    assert retrieved_todo.id == todo.id
    assert retrieved_todo.title == todo.title


def test_get_todo_not_found():
    """Test getting a non-existent todo."""
    storage = InMemoryTodoStorage()
    fake_id = UUID("12345678-1234-5678-1234-567812345678")

    retrieved_todo = storage.get_todo(fake_id)

    assert retrieved_todo is None


def test_get_all_todos():
    """Test getting all todos."""
    storage = InMemoryTodoStorage()
    todo1 = Todo(title="Test task 1")
    todo2 = Todo(title="Test task 2")
    storage.add_todo(todo1)
    storage.add_todo(todo2)

    all_todos = storage.get_all_todos()

    assert len(all_todos) == 2
    assert todo1 in all_todos
    assert todo2 in all_todos


def test_get_all_todos_empty():
    """Test getting all todos when storage is empty."""
    storage = InMemoryTodoStorage()

    all_todos = storage.get_all_todos()

    assert len(all_todos) == 0


def test_update_todo():
    """Test updating a todo in storage."""
    storage = InMemoryTodoStorage()
    todo = Todo(title="Original task")
    storage.add_todo(todo)

    updated_todo = Todo(id=todo.id, title="Updated task")
    result = storage.update_todo(todo.id, updated_todo)

    assert result is not None
    assert result.title == "Updated task"
    assert storage.get_todo(todo.id).title == "Updated task"


def test_update_todo_not_found():
    """Test updating a non-existent todo."""
    storage = InMemoryTodoStorage()
    fake_id = UUID("12345678-1234-5678-1234-567812345678")
    todo = Todo(title="Test task")

    result = storage.update_todo(fake_id, todo)

    assert result is None


def test_delete_todo():
    """Test deleting a todo from storage."""
    storage = InMemoryTodoStorage()
    todo = Todo(title="Test task")
    storage.add_todo(todo)

    result = storage.delete_todo(todo.id)

    assert result is True
    assert storage.get_todo(todo.id) is None


def test_delete_todo_not_found():
    """Test deleting a non-existent todo."""
    storage = InMemoryTodoStorage()
    fake_id = UUID("12345678-1234-5678-1234-567812345678")

    result = storage.delete_todo(fake_id)

    assert result is False


def test_clear_all():
    """Test clearing all todos from storage."""
    storage = InMemoryTodoStorage()
    todo1 = Todo(title="Test task 1")
    todo2 = Todo(title="Test task 2")
    storage.add_todo(todo1)
    storage.add_todo(todo2)

    storage.clear_all()

    assert len(storage.get_all_todos()) == 0
    assert storage.get_todo(todo1.id) is None
    assert storage.get_todo(todo2.id) is None