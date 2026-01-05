from sqlmodel import Session, create_engine
from contextlib import contextmanager
import os
from typing import Generator


# Get database URL from environment, with a default for testing
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/testdb")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """
    Create database tables based on SQLModel models.
    This function should be called on application startup.
    """
    from models import User, Task  # Import here to avoid circular imports
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    Ensures proper cleanup of database connections.
    """
    with Session(engine) as session:
        yield session


def get_session_override():
    """
    Dependency override for testing purposes.
    """
    yield get_session()