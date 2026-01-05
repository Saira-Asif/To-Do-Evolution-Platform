# REST API Endpoints Specification

## API Overview
The Todo Web Application provides a comprehensive REST API for managing user authentication and task management functionality. All endpoints follow RESTful design principles with proper HTTP methods, status codes, and JSON responses.

## API Base URL
```
https://api.todoapp.com/v1/  # Production
http://localhost:8000/      # Development
```

## Authentication
All endpoints except authentication endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Optional success message"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description",
    "details": { /* optional error details */ }
  }
}
```

## Authentication Endpoints

### POST /auth/register
Register a new user account

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "name": "John Doe"
}
```

**Request Validation:**
- email: required, valid email format, unique
- password: required, min 8 chars, mixed case, number, special char
- name: optional, max 100 chars

**Responses:**
- 201 Created: User registered successfully
- 400 Bad Request: Validation errors
- 409 Conflict: Email already exists

**Success Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid-string",
      "email": "user@example.com",
      "name": "John Doe",
      "created_at": "2024-01-01T00:00:00Z"
    },
    "token": "jwt_token_string"
  },
  "message": "User registered successfully"
}
```

### POST /auth/login
Authenticate user and return JWT token

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Responses:**
- 200 OK: Login successful
- 400 Bad Request: Invalid request format
- 401 Unauthorized: Invalid credentials

**Success Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid-string",
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": "jwt_token_string"
  },
  "message": "Login successful"
}
```

### POST /auth/logout
End user session (client-side token removal)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Responses:**
- 200 OK: Logout successful
- 401 Unauthorized: Invalid token

**Success Response:**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

### GET /auth/profile
Get current user's profile information

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Responses:**
- 200 OK: Profile retrieved successfully
- 401 Unauthorized: Invalid token

**Success Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid-string",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

## User-Specific Endpoints

### GET /users/{user_id}/tasks
Get all tasks for a specific user

**URL Parameters:**
- user_id: UUID of the authenticated user (must match JWT token)

**Query Parameters:**
- status: Filter by completion status ("all", "completed", "pending") - default: "all"
- limit: Number of tasks per page (1-100) - default: 20
- offset: Number of tasks to skip - default: 0
- sort: Sort order ("created_at", "updated_at", "title") - default: "created_at"
- order: Sort direction ("asc", "desc") - default: "desc"

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Responses:**
- 200 OK: Tasks retrieved successfully
- 401 Unauthorized: Invalid token
- 403 Forbidden: User ID doesn't match token
- 404 Not Found: User doesn't exist

**Success Response:**
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": "uuid-string",
        "title": "Task title",
        "description": "Task description",
        "completed": false,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      }
    ],
    "pagination": {
      "total": 100,
      "limit": 20,
      "offset": 0,
      "has_more": true
    }
  }
}
```

### POST /users/{user_id}/tasks
Create a new task for the user

**URL Parameters:**
- user_id: UUID of the authenticated user (must match JWT token)

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "title": "New task title",
  "description": "Optional task description",
  "completed": false
}
```

**Request Validation:**
- title: required, 1-255 characters
- description: optional, max 1000 characters
- completed: optional, boolean, default false

**Responses:**
- 201 Created: Task created successfully
- 400 Bad Request: Validation errors
- 401 Unauthorized: Invalid token
- 403 Forbidden: User ID doesn't match token

**Success Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid-string",
    "title": "New task title",
    "description": "Optional task description",
    "completed": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "message": "Task created successfully"
}
```

### GET /users/{user_id}/tasks/{task_id}
Get a specific task for the user

**URL Parameters:**
- user_id: UUID of the authenticated user (must match JWT token)
- task_id: UUID of the task to retrieve

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Responses:**
- 200 OK: Task retrieved successfully
- 401 Unauthorized: Invalid token
- 403 Forbidden: User ID doesn't match token or task doesn't belong to user
- 404 Not Found: Task doesn't exist

**Success Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

### PUT /users/{user_id}/tasks/{task_id}
Update an entire task for the user

**URL Parameters:**
- user_id: UUID of the authenticated user (must match JWT token)
- task_id: UUID of the task to update

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

**Request Validation:**
- title: required, 1-255 characters
- description: optional, max 1000 characters
- completed: required, boolean

**Responses:**
- 200 OK: Task updated successfully
- 400 Bad Request: Validation errors
- 401 Unauthorized: Invalid token
- 403 Forbidden: User ID doesn't match token or task doesn't belong to user
- 404 Not Found: Task doesn't exist

**Success Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid-string",
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-02T00:00:00Z"
  },
  "message": "Task updated successfully"
}
```

### PATCH /users/{user_id}/tasks/{task_id}
Partially update a task for the user

**URL Parameters:**
- user_id: UUID of the authenticated user (must match JWT token)
- task_id: UUID of the task to update

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "title": "Updated task title",
  "completed": true
}
```

**Request Validation:**
- title: optional, 1-255 characters if provided
- description: optional, max 1000 characters if provided
- completed: optional, boolean if provided

**Responses:**
- 200 OK: Task updated successfully
- 400 Bad Request: Validation errors
- 401 Unauthorized: Invalid token
- 403 Forbidden: User ID doesn't match token or task doesn't belong to user
- 404 Not Found: Task doesn't exist

**Success Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid-string",
    "title": "Updated task title",
    "description": "Original task description",
    "completed": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-02T00:00:00Z"
  },
  "message": "Task updated successfully"
}
```

### DELETE /users/{user_id}/tasks/{task_id}
Delete a specific task for the user

**URL Parameters:**
- user_id: UUID of the authenticated user (must match JWT token)
- task_id: UUID of the task to delete

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Responses:**
- 200 OK: Task deleted successfully
- 401 Unauthorized: Invalid token
- 403 Forbidden: User ID doesn't match token or task doesn't belong to user
- 404 Not Found: Task doesn't exist

**Success Response:**
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

### PATCH /users/{user_id}/tasks/{task_id}/toggle-completion
Toggle the completion status of a task

**URL Parameters:**
- user_id: UUID of the authenticated user (must match JWT token)
- task_id: UUID of the task to update

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "completed": true  // Optional: if not provided, will toggle current status
}
```

**Responses:**
- 200 OK: Task completion status updated successfully
- 400 Bad Request: Invalid request format
- 401 Unauthorized: Invalid token
- 403 Forbidden: User ID doesn't match token or task doesn't belong to user
- 404 Not Found: Task doesn't exist

**Success Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description",
    "completed": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-02T00:00:00Z"
  },
  "message": "Task completion status updated successfully"
}
```

## Chatbot Endpoints

### POST /chat/process
Process natural language input and execute task management actions

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "message": "Create a task to buy groceries tomorrow",
  "context": {  // Optional conversation context
    "conversation_id": "uuid-string",
    "previous_intent": "task_creation"
  }
}
```

**Responses:**
- 200 OK: Message processed successfully
- 400 Bad Request: Invalid request format
- 401 Unauthorized: Invalid token
- 422 Unprocessable Entity: Unable to process natural language

**Success Response:**
```json
{
  "success": true,
  "data": {
    "response": "I've created a task 'buy groceries' for tomorrow.",
    "action": {
      "type": "task_created",
      "task": {
        "id": "uuid-string",
        "title": "buy groceries",
        "completed": false,
        "created_at": "2024-01-02T00:00:00Z"
      }
    },
    "context": {
      "conversation_id": "uuid-string",
      "next_expected_input": null
    }
  }
}
```

### GET /chat/capabilities
Get list of supported chatbot capabilities

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Responses:**
- 200 OK: Capabilities retrieved successfully
- 401 Unauthorized: Invalid token

**Success Response:**
```json
{
  "success": true,
  "data": {
    "capabilities": [
      "task_creation",
      "task_completion",
      "task_search",
      "task_modification",
      "due_date_setting"
    ],
    "supported_intents": [
      "create_task",
      "complete_task",
      "search_tasks",
      "update_task",
      "delete_task"
    ]
  }
}
```

## Error Codes

### Authentication Errors
- `AUTH_001`: Invalid credentials
- `AUTH_002`: Token expired
- `AUTH_003`: Invalid token format
- `AUTH_004`: Account locked
- `AUTH_005`: Email already exists

### Task Errors
- `TASK_001`: Task not found
- `TASK_002`: Invalid task data
- `TASK_003`: Insufficient permissions
- `TASK_004`: Task title too long
- `TASK_005`: Task limit exceeded

### General Errors
- `GEN_001`: Validation error
- `GEN_002`: Database error
- `GEN_003`: Server error
- `GEN_004`: Rate limit exceeded
- `GEN_005`: Invalid request

## Rate Limiting
- Authentication endpoints: 10 requests per minute per IP
- Task endpoints: 100 requests per minute per user
- Chatbot endpoints: 50 requests per minute per user

## Versioning
API versioning is handled through URL path (e.g., `/v1/`), with plans for header-based versioning in future versions.