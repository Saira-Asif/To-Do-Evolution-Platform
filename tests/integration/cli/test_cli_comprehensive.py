from click.testing import CliRunner
from unittest.mock import patch
from uuid import UUID
import sys

from src.cli.main import cli
from src.models.storage import InMemoryTodoStorage


def test_cli_full_workflow():
    """Test the full CLI workflow: add, list, update, complete, uncomplete, delete."""
    runner = CliRunner()

    # Create a mock storage to track the todo ID
    storage = InMemoryTodoStorage()

    # Add a task
    result = runner.invoke(cli, ['add', 'Test task', '--desc', 'Test description'])
    assert result.exit_code == 0
    assert 'Added task:' in result.output

    # List tasks
    result = runner.invoke(cli, ['list'])
    assert result.exit_code == 0
    assert 'Test task' in result.output
    assert 'Test description' in result.output

    # Get the ID of the created task for subsequent operations
    # Since we can't easily extract the ID from the output in this test,
    # we'll use the storage directly to get the ID
    todos = storage.get_all_todos()
    assert len(todos) > 0
    task_id = todos[0].id

    # Update the task
    result = runner.invoke(cli, ['update', str(task_id), '--title', 'Updated task'])
    assert result.exit_code == 0
    assert 'Updated task' in result.output

    # Complete the task
    result = runner.invoke(cli, ['complete', str(task_id)])
    assert result.exit_code == 0
    assert 'complete' in result.output

    # Uncomplete the task
    result = runner.invoke(cli, ['uncomplete', str(task_id)])
    assert result.exit_code == 0
    assert 'incomplete' in result.output

    # Delete the task
    with patch('click.confirm', return_value=True):  # Mock confirmation
        result = runner.invoke(cli, ['delete', str(task_id)])
    assert result.exit_code == 0
    assert 'Deleted task' in result.output

    # Verify the task is gone
    result = runner.invoke(cli, ['list'])
    assert result.exit_code == 0
    assert 'No tasks found' in result.output or 'Test task' not in result.output


def test_add_command_with_validation_error():
    """Test the add command with invalid input."""
    runner = CliRunner()

    # Try to add a task with an empty title
    result = runner.invoke(cli, ['add', ''])
    assert result.exit_code == 1
    assert 'Error:' in result.output


def test_update_command_with_invalid_id():
    """Test the update command with an invalid ID."""
    runner = CliRunner()

    # Try to update a task with an invalid UUID
    result = runner.invoke(cli, ['update', 'invalid-id', '--title', 'New title'])
    assert result.exit_code == 1
    assert 'Invalid ID format' in result.output


def test_complete_command_with_invalid_id():
    """Test the complete command with an invalid ID."""
    runner = CliRunner()

    # Try to complete a task with an invalid UUID
    result = runner.invoke(cli, ['complete', 'invalid-id'])
    assert result.exit_code == 1
    assert 'Invalid ID format' in result.output


def test_delete_command_with_invalid_id():
    """Test the delete command with an invalid ID."""
    runner = CliRunner()

    # Try to delete a task with an invalid UUID
    result = runner.invoke(cli, ['delete', 'invalid-id'])
    assert result.exit_code == 1
    assert 'Invalid ID format' in result.output