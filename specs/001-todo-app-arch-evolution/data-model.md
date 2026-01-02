# Data Model: Multi-Phase Todo Application - Console to Cloud

**Feature**: 001-todo-app-arch-evolution
**Date**: 2026-01-02
**Status**: Draft

## Overview

This document defines the data models for the Multi-Phase Todo Application, evolving from simple in-memory structures in Phase I to a full database schema in Phase II and beyond.

## Phase I: In-Memory Data Model

### Todo Model
```python
class Todo:
    id: int
    title: str
    description: str
    status: str  # "pending", "completed", "in-progress"
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
```

### User Model (for future authentication)
```python
class User:
    id: int
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
```

## Phase II: Database Schema (PostgreSQL with SQLModel)

### Todo Model (Enhanced)
```python
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(default="", max_length=1000)
    status: str = Field(default="pending", regex="^(pending|completed|in-progress)$")
    due_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")

    # Relationships
    user: Optional["User"] = Relationship(back_populates="todos")
```

### User Model (with authentication)
```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(min_length=3, max_length=50, unique=True)
    email: str = Field(regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", unique=True)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Relationships
    todos: List[Todo] = Relationship(back_populates="user")
```

## Phase III: AI Integration Data Models

### AI Intent Model
```python
class AIIntent:
    intent_type: str  # "create_todo", "update_todo", "delete_todo", "list_todos"
    entities: Dict[str, Any]  # Extracted entities like dates, priorities, etc.
    confidence: float  # Confidence score for the intent
    original_query: str  # The original user query
    processed_at: datetime
```

### Conversation Context Model
```python
class ConversationContext:
    session_id: str
    user_id: int
    current_intent: Optional[str]
    previous_context: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
```

## Phase IV & V: Infrastructure Data Models

### Deployment Configuration Model
```python
class DeploymentConfig:
    service_name: str
    replicas: int
    resource_limits: Dict[str, str]  # CPU, memory limits
    environment: str  # "dev", "staging", "prod"
    health_check_path: str
    readiness_probe: Dict[str, Any]
    liveness_probe: Dict[str, Any]
```

### Event Model (for Kafka in Phase V)
```python
class TodoEvent:
    event_id: str
    event_type: str  # "todo_created", "todo_updated", "todo_deleted"
    todo_id: int
    user_id: int
    payload: Dict[str, Any]  # The actual todo data
    timestamp: datetime
    source_service: str
```

## Validation Rules

### Todo Validation
- Title: Required, 1-255 characters
- Description: Optional, 0-1000 characters
- Status: Must be one of "pending", "completed", "in-progress"
- Due date: If provided, must be a future date
- User ID: Must reference an existing user

### User Validation
- Username: 3-50 characters, unique
- Email: Valid email format, unique
- Password: Hashed using secure algorithm
- Active status: Boolean indicating account status

## Relationships

### Todo → User
- Many-to-One: Multiple todos can belong to one user
- Foreign key: `user_id` in Todo table references `id` in User table
- Cascade behavior: When user is deleted, their todos are also deleted

## Indexes

### Todo Table
- Primary: `id`
- Foreign: `user_id`
- Composite: `(user_id, status)` for efficient filtering
- Additional: `due_date` for sorting and filtering

### User Table
- Primary: `id`
- Unique: `username`
- Unique: `email`
- Additional: `is_active` for filtering active users

## Migration Strategy

### Phase I → Phase II
- Data migration from in-memory dict to PostgreSQL
- Schema creation for Todo and User tables
- Data validation during migration

### Phase II → Phase III
- Addition of AI-related tables (AIIntent, ConversationContext)
- No breaking changes to existing Todo/User models

### Phase III → Phase IV/V
- Addition of infrastructure-related models
- Event sourcing models for Kafka integration
- Monitoring and configuration models

## Security Considerations

### Data Encryption
- Sensitive data (passwords) stored as hashed values
- PII (email) stored in encrypted form where required
- Connection to database uses SSL/TLS

### Access Control
- All data access through authenticated endpoints
- Row-level security based on user ownership
- Audit logging for sensitive operations

## Performance Considerations

### Query Optimization
- Proper indexing for common query patterns
- Pagination for large result sets
- Caching for frequently accessed data

### Scalability
- Horizontal partitioning by user_id for large datasets
- Read replicas for read-heavy operations
- Connection pooling for database connections

## Data Lifecycle

### Creation
- Todos created with current timestamp
- Validation occurs before persistence
- Default status set to "pending"

### Updates
- Updated timestamp automatically updated
- Change tracking for audit purposes
- Validation on all updates

### Deletion
- Soft delete option for audit trail
- Hard delete for security-sensitive data
- Cleanup jobs for soft-deleted records

## API Contracts

### Todo API
- GET /todos - List user's todos with filtering
- POST /todos - Create new todo
- GET /todos/{id} - Get specific todo
- PUT /todos/{id} - Update todo
- DELETE /todos/{id} - Delete todo

### User API
- POST /auth/register - User registration
- POST /auth/login - User authentication
- GET /auth/profile - Get user profile
- PUT /auth/profile - Update user profile

This data model provides the foundation for all phases of the application, with clear evolution paths and compatibility between phases.