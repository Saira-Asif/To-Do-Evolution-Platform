# REST API Contract - Phase II: Full-Stack Web Application with Authentication

## Overview
This document defines the REST API contract for the Full-Stack Web Application with Authentication. It specifies the endpoints, request/response formats, authentication requirements, and error handling patterns.

## API Base Information
- **Base URL**: `/api/{user_id}/`
- **Protocol**: HTTPS (in production)
- **Content-Type**: `application/json`
- **Authentication**: JWT Bearer tokens required for all endpoints
- **Version**: 1.0

## Authentication Requirements
All API endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

The user_id in the URL must match the user_id in the JWT token payload.

## Common HTTP Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource successfully created
- `204 No Content`: Request successful, no content to return
- `400 Bad Request`: Invalid request format or validation error
- `401 Unauthorized`: Invalid or missing authentication token
- `403 Forbidden`: Valid token but insufficient permissions
- `404 Not Found`: Requested resource does not exist
- `422 Unprocessable Entity`: Validation error in request body
- `500 Internal Server Error`: Server error

## Common Error Response Format
```json
{
  "detail": "Error message describing the issue",
  "error_code": "ERROR_CODE_STRING",
  "timestamp": "2026-01-05T10:30:00Z"
}
```

## Endpoint Specifications

### 1. List User Tasks
- **Endpoint**: `GET /api/{user_id}/tasks`
- **Description**: Retrieve all tasks for the specified user
- **Authentication**: Required (JWT token must match user_id)
- **Path Parameters**:
  - `user_id` (string): The ID of the user whose tasks to retrieve
- **Query Parameters**:
  - `completed` (string, optional): Filter by completion status ("true", "false", or omit for all)
  - `limit` (integer, optional): Maximum number of tasks to return (default: 50, max: 100)
  - `offset` (integer, optional): Number of tasks to skip (for pagination)
- **Request Headers**:
  - `Authorization: Bearer <token>`
- **Success Response** (200):
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "user123",
      "title": "Complete project documentation",
      "description": "Write comprehensive docs for the project",
      "completed": false,
      "created_at": "2026-01-05T10:30:00Z",
      "updated_at": "2026-01-05T10:30:00Z"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```
- **Error Responses**:
  - `401`: Invalid or missing token
  - `403`: Token user_id doesn't match URL user_id

### 2. Create Task
- **Endpoint**: `POST /api/{user_id}/tasks`
- **Description**: Create a new task for the specified user
- **Authentication**: Required (JWT token must match user_id)
- **Path Parameters**:
  - `user_id` (string): The ID of the user creating the task
- **Request Headers**:
  - `Authorization: Bearer <token>`
- **Request Body**:
```json
{
  "title": "Task title",
  "description": "Optional task description"
}
```
- **Success Response** (201):
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Task title",
  "description": "Optional task description",
  "completed": false,
  "created_at": "2026-01-05T10:30:00Z",
  "updated_at": "2026-01-05T10:30:00Z"
}
```
- **Validation Rules**:
  - `title` is required, 1-200 characters
  - `description` is optional, max 1000 characters
- **Error Responses**:
  - `400`: Invalid request body format
  - `401`: Invalid or missing token
  - `403`: Token user_id doesn't match URL user_id
  - `422`: Validation errors

### 3. Get Task Details
- **Endpoint**: `GET /api/{user_id}/tasks/{id}`
- **Description**: Retrieve details of a specific task
- **Authentication**: Required (JWT token must match user_id)
- **Path Parameters**:
  - `user_id` (string): The ID of the task owner
  - `id` (integer): The ID of the task to retrieve
- **Request Headers**:
  - `Authorization: Bearer <token>`
- **Success Response** (200):
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "created_at": "2026-01-05T10:30:00Z",
  "updated_at": "2026-01-05T10:30:00Z"
}
```
- **Error Responses**:
  - `401`: Invalid or missing token
  - `403`: Token user_id doesn't match URL user_id
  - `404`: Task not found

### 4. Update Task
- **Endpoint**: `PUT /api/{user_id}/tasks/{id}`
- **Description**: Update an existing task
- **Authentication**: Required (JWT token must match user_id)
- **Path Parameters**:
  - `user_id` (string): The ID of the task owner
  - `id` (integer): The ID of the task to update
- **Request Headers**:
  - `Authorization: Bearer <token>`
- **Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```
- **Success Response** (200):
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true,
  "created_at": "2026-01-05T10:30:00Z",
  "updated_at": "2026-01-05T11:00:00Z"
}
```
- **Validation Rules**:
  - `title` (if provided) must be 1-200 characters
  - `description` (if provided) must be max 1000 characters
  - `completed` (if provided) must be boolean
- **Error Responses**:
  - `400`: Invalid request body format
  - `401`: Invalid or missing token
  - `403`: Token user_id doesn't match URL user_id
  - `404`: Task not found
  - `422`: Validation errors

### 5. Delete Task
- **Endpoint**: `DELETE /api/{user_id}/tasks/{id}`
- **Description**: Delete a specific task
- **Authentication**: Required (JWT token must match user_id)
- **Path Parameters**:
  - `user_id` (string): The ID of the task owner
  - `id` (integer): The ID of the task to delete
- **Request Headers**:
  - `Authorization: Bearer <token>`
- **Success Response** (204): No content
- **Error Responses**:
  - `401`: Invalid or missing token
  - `403`: Token user_id doesn't match URL user_id
  - `404`: Task not found

### 6. Toggle Task Completion
- **Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`
- **Description**: Toggle the completion status of a task
- **Authentication**: Required (JWT token must match user_id)
- **Path Parameters**:
  - `user_id` (string): The ID of the task owner
  - `id` (integer): The ID of the task to update
- **Request Headers**:
  - `Authorization: Bearer <token>`
- **Request Body**:
```json
{
  "completed": true
}
```
- **Success Response** (200):
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Task title",
  "description": "Task description",
  "completed": true,
  "created_at": "2026-01-05T10:30:00Z",
  "updated_at": "2026-01-05T11:00:00Z"
}
```
- **Validation Rules**:
  - `completed` is required and must be boolean
- **Error Responses**:
  - `400`: Invalid request body format
  - `401`: Invalid or missing token
  - `403`: Token user_id doesn't match URL user_id
  - `404`: Task not found
  - `422`: Validation errors

## Data Validation Rules

### Task Title
- Required for creation
- 1-200 characters
- No control characters
- Trimmed of leading/trailing whitespace

### Task Description
- Optional
- Max 1000 characters if provided
- No control characters
- May be null

### Task Completion Status
- Boolean value (true/false)
- Default: false for new tasks
- Can be updated to true or false

### User ID
- Must match the authenticated user
- Verified against JWT token
- Must exist in the system

## Security Requirements

### Authentication
- All endpoints require valid JWT token
- Token must be included in Authorization header
- Token must be properly formatted
- Token must not be expired

### Authorization
- User can only access their own tasks
- user_id in URL must match user_id in JWT token
- 403 Forbidden returned for unauthorized access attempts

### Data Validation
- All input validated before database operations
- SQL injection protection through parameterized queries
- Input sanitization applied where appropriate

## Error Handling

### Client Errors (4xx)
- Invalid request format returns 400
- Missing authentication returns 401
- Insufficient permissions returns 403
- Non-existent resources return 404
- Validation failures return 422

### Server Errors (5xx)
- Internal server errors return 500
- Error messages do not expose internal system details
- All errors logged for debugging purposes

## Performance Considerations

### Rate Limiting
- API endpoints subject to rate limiting
- Default: 100 requests per minute per user

### Pagination
- List endpoints support pagination
- Default limit: 50 items
- Maximum limit: 100 items

### Caching
- Response caching may be implemented for read operations
- Cache invalidation on write operations