from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import User, UserCreate
from database import get_session
from services.user_service import create_user
from auth import create_access_token
import bcrypt
from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=User)
def register_user(
    user_create: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Register a new user.
    This endpoint creates a new user account with the provided details.
    """
    return create_user(session, user_create)


@router.post("/login")
def login_user(
    login_request: LoginRequest,
    session: Session = Depends(get_session)
):
    """
    Login a user.
    This endpoint authenticates a user and returns an access token.
    """
    # Find user by email
    user = session.exec(select(User).where(User.email == login_request.email)).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Verify password
    if not bcrypt.checkpw(login_request.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # Create access token
    token_data = {"sub": user.id}
    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }