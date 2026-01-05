# Backend - Claude Code Instructions

## Overview
This is the FastAPI backend for the Todo Web Application with authentication and PostgreSQL database.

## Technology Stack
- **Framework**: FastAPI with async/await patterns
- **ORM**: SQLModel (combines SQLAlchemy and Pydantic)
- **Authentication**: JWT-based with custom middleware
- **Database**: PostgreSQL (Neon DB compatible)

## Project Structure
- `main.py` - FastAPI application entry point
- `models.py` - SQLModel database models with Pydantic validation
- `database.py` - Database connection and session management
- `routes/` - API route definitions
- `services/` - Business logic implementation
- `middleware/` - Authentication and authorization middleware
- `auth.py` - JWT token handling utilities

## Key Patterns
- Use SQLModel for database models with Pydantic validation
- Implement async database operations for performance
- Follow dependency injection patterns for service layer
- Use Pydantic models for request/response validation
- Implement proper error handling with appropriate HTTP status codes
- Use FastAPI's built-in automatic API documentation (Swagger/OpenAPI)

## Authentication Flow
- JWT tokens are generated upon successful login
- Middleware validates JWT tokens for protected endpoints
- User ID from JWT is matched against URL parameter for authorization
- All database queries are filtered by authenticated user

## API Design
- RESTful endpoints following standard HTTP methods
- User ID included in URL path for context (e.g., `/api/{user_id}/tasks`)
- Consistent response format with proper error handling
- Input validation using Pydantic models
- Proper HTTP status codes (200, 201, 204, 400, 401, 403, 404, 422, 500)

## Common Commands
- `uvicorn main:app --reload` - Start development server
- `pytest` - Run tests
- `pytest --cov=.` - Run tests with coverage
- `mypy .` - Run type checking
- `black .` - Format code

## Security Considerations
- All endpoints requiring authentication must validate JWT tokens
- User data isolation through user_id filtering
- Input validation to prevent injection attacks
- Proper error message handling to avoid information leakage