"""
Database schema setup for the Todo Web Application.
This module contains functions to initialize the database schema.
"""

from sqlmodel import SQLModel
from database import engine
from models import User, Task


def create_initial_schema():
    """
    Create the initial database schema.
    This function creates all tables defined in the models.
    """
    print("Creating database schema...")
    SQLModel.metadata.create_all(engine)
    print("Database schema created successfully.")


if __name__ == "__main__":
    create_initial_schema()