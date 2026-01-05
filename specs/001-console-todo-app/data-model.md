# Data Model - Console Todo App

## Overview
This document defines the data structures and models used in the Console Todo Application.

## Todo Item Model

### Core Attributes
- **id**: Unique identifier for each todo item (string/UUID)
- **title**: The main text/description of the todo item (string, required)
- **completed**: Boolean indicating whether the task is completed (boolean, default: false)
- **created_at**: Timestamp when the todo was created (datetime, auto-generated)
- **updated_at**: Timestamp when the todo was last modified (datetime, auto-generated)
- **due_date**: Optional due date for the todo item (datetime, optional)
- **priority**: Priority level of the task (string: "low", "medium", "high", default: "medium")

### Example JSON Representation
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Complete project documentation",
  "completed": false,
  "created_at": "2026-01-05T10:30:00Z",
  "updated_at": "2026-01-05T10:30:00Z",
  "due_date": "2026-01-10T23:59:59Z",
  "priority": "high"
}
```

## Storage Model

### File Structure
- **Location**: `~/.todo_app/todos.json` (or platform-appropriate config directory)
- **Format**: JSON array containing all todo items
- **Encoding**: UTF-8

### File Schema
```json
{
  "version": "1.0",
  "todos": [
    {
      "id": "string",
      "title": "string",
      "completed": "boolean",
      "created_at": "string (ISO 8601)",
      "updated_at": "string (ISO 8601)",
      "due_date": "string (ISO 8601) or null",
      "priority": "string"
    }
  ]
}
```

## Validation Rules

### Todo Item Validation
1. **Title**: Must be non-empty string with maximum 500 characters
2. **Priority**: Must be one of "low", "medium", "high"
3. **Due Date**: If provided, must be a valid ISO 8601 datetime string
4. **ID**: Must be a valid UUID v4 format
5. **Timestamps**: Must be valid ISO 8601 datetime strings

### Constraints
- Maximum of 10,000 todos per user (to prevent performance issues)
- Title must not contain control characters
- Due date cannot be in the past when creating/updating (optional validation)

## Data Operations

### Create
- Generate new UUID for ID
- Set `created_at` and `updated_at` to current timestamp
- Set `completed` to false by default
- Validate all required fields

### Read
- Fetch all todos or filter by specific criteria
- Support sorting by creation date, due date, or priority
- Support pagination for large datasets

### Update
- Update `updated_at` timestamp
- Validate changes against validation rules
- Preserve `created_at` timestamp

### Delete
- Remove item from storage
- Update any related metadata

## Migration Considerations

### Version 1.0 to Future Versions
- Plan for backward compatibility
- Support for additional fields in future versions
- Migration scripts for schema changes