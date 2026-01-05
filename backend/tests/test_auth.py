"""
Basic authentication tests for the Todo Web Application.
This file contains basic tests for user registration and authentication.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from main import app
from models import User
from database import engine


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_register_user(client: TestClient):
    """
    Test user registration endpoint.
    """
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"


def test_login_user(client: TestClient):
    """
    Test user login endpoint.
    """
    # First register a user
    client.post("/api/auth/register", json={
        "email": "login@example.com",
        "password": "testpassword123",
        "name": "Login User"
    })

    # Then try to login
    response = client.post("/api/auth/login", json={
        "email": "login@example.com",
        "password": "testpassword123"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data