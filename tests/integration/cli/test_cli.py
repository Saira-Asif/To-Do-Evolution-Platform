import pytest
from unittest.mock import Mock, patch
from io import StringIO
from src.cli.main import create_cli_app


class TestCLI:
    """Integration tests for CLI functionality"""

    def test_cli_creation(self):
        """Test that CLI app can be created successfully."""
        app = create_cli_app()

        # The function should return a callable
        assert callable(app)

    # Additional CLI tests would require more complex mocking of Rich and input/output
    # For now, we'll focus on ensuring the basic structure is in place