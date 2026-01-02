import pytest
from unittest.mock import patch, MagicMock
from src.cli.main import main


class TestCLIMainSimple:
    """Simple tests for CLI main function"""

    @patch('src.cli.main.create_cli_app')
    def test_main_function_calls_app(self, mock_create_cli_app):
        """Test that main function calls the CLI app."""
        # Create a mock app that does nothing
        mock_app = MagicMock()
        mock_create_cli_app.return_value = mock_app

        # Call main function
        main()

        # Verify that create_cli_app was called
        mock_create_cli_app.assert_called_once()

        # Verify that the returned app was called
        mock_app.assert_called_once()