# Data Model - Phase II: Full-Stack Web Application with Authentication

## Overview
This document defines the data structures and models for the Full-Stack Web Application with Authentication. It outlines the entities, their relationships, and validation rules based on the feature specification.

## Entity Models

### User Entity
The User entity is primarily managed by Better Auth, but we define the interface for integration purposes.

#### Attributes
- **id**: string (Primary Key)
  - Globally unique identifier for the user
  - Format: UUID or Better Auth user ID
  - Required: Yes

- **email**: string
  - User's email address for authentication
  - Format: Valid email format
  - Required: Yes
  - Unique: Yes

- **name**: string
  - User's display name
  - Format: Text
  - Required: No
  - Max length: 100 characters

- **created_at**: timestamp
  - Time when user account was created
  - Format: ISO 8601 datetime
  - Required: Yes
  - Auto-generated: Yes

#### Relationships
- One-to-Many: User → Tasks (user has many tasks)

#### Validation Rules
- Email must be valid email format
- Email must be unique across all users
- Name (if provided) must be 1-100 characters

### Task Entity
The Task entity represents individual todo items owned by a user.

#### Attributes
- **id**: integer (Primary Key)
  - Unique identifier for the task
  - Auto-incrementing
  - Required: Yes

- **user_id**: string (Foreign Key)
  - Reference to the owning user
  - Links to User.id
  - Required: Yes

- **title**: string
  - Main text/description of the task
  - Required: Yes
  - Min length: 1 character
  - Max length: 200 characters

- **description**: text (optional)
  - Additional details about the task
  - Required: No
  - Max length: 1000 characters

- **completed**: boolean
  - Indicates whether the task is completed
  - Default: false
  - Required: Yes

- **created_at**: timestamp
  - Time when task was created
  - Format: ISO 8601 datetime
  - Required: Yes
  - Auto-generated: Yes

- **updated_at**: timestamp
  - Time when task was last modified
  - Format: ISO 8601 datetime
  - Required: Yes
  - Auto-generated/Updated: Yes

#### Relationships
- Many-to-One: Task → User (task belongs to one user)

#### Validation Rules
- Title must be 1-200 characters
- Description (if provided) must be max 1000 characters
- user_id must reference an existing user
- completed must be boolean value
- created_at and updated_at are automatically managed

#### State Transitions
- New Task: completed = false (default)
- Task Completion: completed changes from false to true
- Task Reversion: completed changes from true to false

## API Data Transfer Objects (DTOs)

### Task Creation DTO
Used for creating new tasks via API

#### Attributes
- **title**: string (required, 1-200 characters)
- **description**: string (optional, max 1000 characters)

### Task Update DTO
Used for updating existing tasks via API

#### Attributes
- **title**: string (optional, 1-200 characters)
- **description**: string (optional, max 1000 characters)
- **completed**: boolean (optional)

### Task Response DTO
Used for returning task data via API

#### Attributes
- **id**: integer
- **user_id**: string
- **title**: string
- **description**: string or null
- **completed**: boolean
- **created_at**: string (ISO 8601)
- **updated_at**: string (ISO 8601)

### Authentication DTOs
Managed by Better Auth but defined for API integration:

#### Login Request DTO
- **email**: string (required)
- **password**: string (required)

#### Login Response DTO
- **token**: string (JWT token)
- **user**: User object with id and email

## Database Schema

### PostgreSQL Tables

```sql
-- Users table (managed by Better Auth)
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Index for user_id for efficient querying
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

## Data Validation Rules

### Input Validation
- All API inputs must be validated before processing
- Title: Required, 1-200 characters, no control characters
- Description: Optional, max 1000 characters
- user_id: Must be valid user identifier
- completed: Must be boolean value

### Business Logic Validation
- Users can only access their own tasks
- Users can only modify their own tasks
- Users can only delete their own tasks
- Task ownership cannot be transferred

## API Contract Definitions

### Task API Endpoints

#### GET /api/{user_id}/tasks
- **Purpose**: List all tasks for a specific user
- **Response**: Array of Task Response DTOs
- **Authentication**: JWT token required and must match user_id

#### POST /api/{user_id}/tasks
- **Purpose**: Create a new task for a user
- **Request Body**: Task Creation DTO
- **Response**: Task Response DTO
- **Authentication**: JWT token required and must match user_id

#### GET /api/{user_id}/tasks/{id}
- **Purpose**: Get specific task details
- **Response**: Task Response DTO
- **Authentication**: JWT token required and must match user_id

#### PUT /api/{user_id}/tasks/{id}
- **Purpose**: Update an existing task
- **Request Body**: Task Update DTO
- **Response**: Task Response DTO
- **Authentication**: JWT token required and must match user_id

#### DELETE /api/{user_id}/tasks/{id}
- **Purpose**: Delete a task
- **Response**: Success status
- **Authentication**: JWT token required and must match user_id

#### PATCH /api/{user_id}/tasks/{id}/complete
- **Purpose**: Toggle task completion status
- **Response**: Task Response DTO
- **Authentication**: JWT token required and must match user_id

## Security Considerations

### Data Access
- All queries must be filtered by authenticated user_id
- Cross-user data access must be prevented
- JWT token must be validated for each request
- User_id in URL must match user_id in JWT token

### Data Integrity
- Foreign key constraints enforce referential integrity
- CASCADE DELETE ensures cleanup of user's tasks when user is deleted
- Timestamps automatically managed to track changes