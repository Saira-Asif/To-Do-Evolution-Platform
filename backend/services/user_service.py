from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
import bcrypt
from models import User, UserCreate
from fastapi import HTTPException


def create_user(session: Session, user_create: UserCreate) -> User:
    """
    Create a new user with proper validation and password hashing.
    """
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = bcrypt.hashpw(user_create.password.encode('utf-8'), bcrypt.gensalt())

    # Create new user
    user = User(
        email=user_create.email,
        name=user_create.name,
        hashed_password=hashed_password.decode('utf-8'),
        created_at=datetime.utcnow()
    )

    # Add to database
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """
    Get a user by their email address.
    """
    user = session.exec(select(User).where(User.email == email)).first()
    return user