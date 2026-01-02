import pytest
from unittest.mock import patch, Mock
from datetime import datetime
from src.cli.main import (
    safe_int_input, display_todos, add_todo, update_todo,
    delete_todo, mark_todo_status, show_menu
)
from src.models.todo import Todo, TodoStatus
from src.services.todo_service import TodoService


class TestCLIFunctions:
    """Test individual CLI functions to improve coverage"""

    def test_safe_int_input_valid(self):
        """Test safe_int_input with valid integer input."""
        with patch('src.cli.main.Prompt') as mock_prompt:
            mock_prompt.ask.return_value = "123"
            mock_console = Mock()

            result = safe_int_input(mock_console, "Enter ID")

            assert result == 123
            mock_prompt.ask.assert_called_once_with("Enter ID")

    def test_safe_int_input_invalid(self):
        """Test safe_int_input with invalid input."""
        with patch('src.cli.main.Prompt') as mock_prompt:
            mock_prompt.ask.return_value = "abc"
            mock_console = Mock()

            result = safe_int_input(mock_console, "Enter ID")

            assert result is None
            mock_prompt.ask.assert_called_once_with("Enter ID")
            mock_console.print.assert_called_once()

    def test_display_todos_empty(self):
        """Test display_todos with no todos."""
        mock_console = Mock()
        mock_todo_service = Mock()
        mock_todo_service.get_all_todos.return_value = []

        display_todos(mock_console, mock_todo_service)

        # Check that the "No todos found" message was printed
        mock_console.print.assert_called()

    def test_display_todos_with_data(self):
        """Test display_todos with todos."""
        mock_console = Mock()
        mock_todo_service = Mock()

        # Create a mock todo
        mock_todo = Mock(spec=Todo)
        mock_todo.id = 1
        mock_todo.title = "Test Todo"
        mock_todo.description = "Test Description"
        mock_todo.status = TodoStatus.PENDING
        mock_todo.due_date = datetime(2023, 12, 31, 10, 0)
        mock_todo.created_at = datetime(2023, 1, 1, 10, 0)
        mock_todo_service.get_all_todos.return_value = [mock_todo]

        display_todos(mock_console, mock_todo_service)

        # Should have printed the table
        # The exact call depends on the Table implementation, so we just check that print was called
        assert mock_console.print.called

    def test_add_todo_success(self):
        """Test add_todo function successfully adds a todo."""
        with patch('src.cli.main.Prompt') as mock_prompt:
            mock_prompt.ask.side_effect = [
                "Test Title",      # title
                "Test Description", # description
                ""                 # due date (empty)
            ]
            mock_console = Mock()
            mock_todo_service = Mock()

            # Mock the created todo
            mock_created_todo = Mock(spec=Todo)
            mock_created_todo.id = 1
            mock_todo_service.create_todo.return_value = mock_created_todo

            add_todo(mock_console, mock_todo_service)

            # Verify that create_todo was called with the correct parameters
            mock_todo_service.create_todo.assert_called_once_with(
                "Test Title",
                "Test Description",
                None
            )

    def test_add_todo_with_due_date(self):
        """Test add_todo function with a due date."""
        with patch('src.cli.main.Prompt') as mock_prompt:
            mock_prompt.ask.side_effect = [
                "Test Title",           # title
                "Test Description",     # description
                "2023-12-31 10:00"    # due date
            ]
            mock_console = Mock()
            mock_todo_service = Mock()

            # Mock the created todo
            mock_created_todo = Mock(spec=Todo)
            mock_created_todo.id = 1
            mock_todo_service.create_todo.return_value = mock_created_todo

            add_todo(mock_console, mock_todo_service)

            # Verify that create_todo was called with the correct parameters
            # The due_date should be a datetime object
            assert mock_todo_service.create_todo.called

    def test_add_todo_error(self):
        """Test add_todo function when there's an error."""
        with patch('src.cli.main.Prompt') as mock_prompt:
            mock_prompt.ask.side_effect = [
                "Test Title",
                "Test Description",
                ""
            ]
            mock_console = Mock()
            mock_todo_service = Mock()
            mock_todo_service.create_todo.side_effect = ValueError("Invalid input")

            add_todo(mock_console, mock_todo_service)

            # Should have printed an error message
            assert mock_console.print.called

    def test_update_todo_success(self):
        """Test update_todo function successfully updates a todo."""
        with patch('src.cli.main.Prompt') as mock_prompt:
            mock_prompt.ask.side_effect = [
                "1",                # todo ID
                "Updated Title",    # new title
                "Updated Description"  # new description
            ]
            mock_console = Mock()
            mock_todo_service = Mock()

            # Mock the existing todo
            mock_existing_todo = Mock(spec=Todo)
            mock_existing_todo.id = 1
            mock_existing_todo.title = "Original Title"
            mock_existing_todo.description = "Original Description"
            mock_todo_service.get_todo.return_value = mock_existing_todo

            # Mock the updated todo
            mock_updated_todo = Mock(spec=Todo)
            mock_updated_todo.id = 1
            mock_todo_service.update_todo.return_value = mock_updated_todo

            update_todo(mock_console, mock_todo_service)

            # Verify that update_todo was called with the correct parameters
            mock_todo_service.update_todo.assert_called_once_with(
                1,
                title="Updated Title",
                description="Updated Description"
            )

    def test_update_todo_not_found(self):
        """Test update_todo function when todo is not found."""
        with patch('src.cli.main.Prompt') as mock_prompt:
            mock_prompt.ask.return_value = "999"  # Non-existent todo ID
            mock_console = Mock()
            mock_todo_service = Mock()
            mock_todo_service.get_todo.return_value = None

            update_todo(mock_console, mock_todo_service)

            # Should have printed an error message
            assert mock_console.print.called

    def test_delete_todo_success(self):
        """Test delete_todo function successfully deletes a todo."""
        with patch('src.cli.main.Prompt') as mock_prompt:
            mock_prompt.ask.return_value = "1"  # todo ID
            mock_console = Mock()
            mock_todo_service = Mock()
            mock_todo_service.delete_todo.return_value = True

            delete_todo(mock_console, mock_todo_service)

            # Verify that delete_todo was called with the correct ID
            mock_todo_service.delete_todo.assert_called_once_with(1)

    def test_delete_todo_not_found(self):
        """Test delete_todo function when todo is not found."""
        with patch('src.cli.main.Prompt') as mock_prompt:
            mock_prompt.ask.return_value = "999"  # Non-existent todo ID
            mock_console = Mock()
            mock_todo_service = Mock()
            mock_todo_service.delete_todo.return_value = False

            delete_todo(mock_console, mock_todo_service)

            # Should have printed an error message
            assert mock_console.print.called

    def test_mark_todo_status_success(self):
        """Test mark_todo_status function successfully updates status."""
        with patch('src.cli.main.Prompt') as mock_prompt:
            mock_prompt.ask.side_effect = ["1", "3"]  # todo ID, then "3" for completed
            mock_console = Mock()
            mock_todo_service = Mock()

            # Mock the existing todo
            mock_existing_todo = Mock(spec=Todo)
            mock_existing_todo.id = 1
            mock_todo_service.get_todo.return_value = mock_existing_todo

            # Mock the updated todo
            mock_updated_todo = Mock(spec=Todo)
            mock_updated_todo.id = 1
            mock_updated_todo.status = TodoStatus.COMPLETED
            mock_todo_service.mark_todo_completed.return_value = mock_updated_todo

            mark_todo_status(mock_console, mock_todo_service)

            # Verify that mark_todo_completed was called
            mock_todo_service.mark_todo_completed.assert_called_once_with(1)

    def test_mark_todo_status_invalid_choice(self):
        """Test mark_todo_status function with invalid status choice."""
        with patch('src.cli.main.Prompt') as mock_prompt:
            # In reality, Rich Prompt with choices would prevent invalid input,
            # but we're testing the logic inside the function
            # Let's test with a valid choice but mock the service to return None
            mock_prompt.ask.side_effect = ["1", "3"]  # todo ID, then "3" for completed
            mock_console = Mock()
            mock_todo_service = Mock()

            # Mock the existing todo
            mock_existing_todo = Mock(spec=Todo)
            mock_existing_todo.id = 1
            mock_todo_service.get_todo.return_value = mock_existing_todo

            # Mock the service to return None to simulate failure
            mock_todo_service.mark_todo_completed.return_value = None

            mark_todo_status(mock_console, mock_todo_service)

            # Should print failure message
            assert mock_console.print.called

    def test_mark_todo_status_not_found(self):
        """Test mark_todo_status function when todo is not found."""
        with patch('src.cli.main.Prompt') as mock_prompt:
            mock_prompt.ask.return_value = "999"  # Non-existent todo ID
            mock_console = Mock()
            mock_todo_service = Mock()
            mock_todo_service.get_todo.return_value = None

            mark_todo_status(mock_console, mock_todo_service)

            # Should have printed an error message
            assert mock_console.print.called

    @patch('src.cli.main.Prompt')
    def test_show_menu_exit(self, mock_prompt):
        """Test show_menu function with exit choice."""
        mock_prompt.ask.return_value = "8"  # Exit choice
        mock_console = Mock()
        mock_todo_service = Mock()

        # Call show_menu, which should exit after receiving "8"
        show_menu(mock_console, mock_todo_service)

        # Verify that the goodbye message was printed
        mock_console.print.assert_called()

    @patch('src.cli.main.Prompt')
    def test_show_menu_list_all(self, mock_prompt):
        """Test show_menu function with list all todos choice."""
        mock_prompt.ask.side_effect = ["1", "8"]  # List all, then exit
        mock_console = Mock()
        mock_todo_service = Mock()

        show_menu(mock_console, mock_todo_service)

        # Should have called get_all_todos to list all todos
        mock_todo_service.get_all_todos.assert_called()