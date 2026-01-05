# MCP Tools API Specification

## Overview
Model Context Protocol (MCP) tools provide an interface for AI assistants to interact with the Todo Web Application. These tools enable AI systems to perform operations on behalf of users while maintaining proper authentication and authorization.

## Tool Registration
The application exposes available tools through the MCP discovery endpoint:
```
GET /.well-known/mcp/tools
```

## Authentication
All MCP tools require a valid JWT token passed in the tool call parameters. The token must be validated for each tool invocation to ensure proper user context and permissions.

## Available Tools

### 1. create-task
Create a new task for the authenticated user.

**Tool Name:** `create-task`

**Description:** Creates a new task with the specified title and optional description for the authenticated user.

**Parameters:**
```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "Task title (required, 1-255 characters)",
      "minLength": 1,
      "maxLength": 255
    },
    "description": {
      "type": "string",
      "description": "Optional task description (max 1000 characters)",
      "maxLength": 1000
    },
    "token": {
      "type": "string",
      "description": "JWT authentication token"
    }
  },
  "required": ["title", "token"]
}
```

**Result Schema:**
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the operation was successful"
    },
    "task": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique task identifier"
        },
        "title": {
          "type": "string",
          "description": "Task title"
        },
        "description": {
          "type": "string",
          "description": "Task description"
        },
        "completed": {
          "type": "boolean",
          "description": "Whether task is completed"
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "description": "Task creation timestamp"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "description": "Task update timestamp"
        }
      }
    },
    "error": {
      "type": "string",
      "description": "Error message if operation failed"
    }
  }
}
```

### 2. list-tasks
Retrieve a list of tasks for the authenticated user.

**Tool Name:** `list-tasks`

**Description:** Retrieves a paginated list of tasks for the authenticated user with optional filtering.

**Parameters:**
```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["all", "completed", "pending"],
      "description": "Filter tasks by completion status (default: all)",
      "default": "all"
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100,
      "description": "Number of tasks per page (default: 20)",
      "default": 20
    },
    "offset": {
      "type": "integer",
      "minimum": 0,
      "description": "Number of tasks to skip (default: 0)",
      "default": 0
    },
    "token": {
      "type": "string",
      "description": "JWT authentication token"
    }
  },
  "required": ["token"]
}
```

**Result Schema:**
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the operation was successful"
    },
    "tasks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string",
            "description": "Unique task identifier"
          },
          "title": {
            "type": "string",
            "description": "Task title"
          },
          "description": {
            "type": "string",
            "description": "Task description"
          },
          "completed": {
            "type": "boolean",
            "description": "Whether task is completed"
          },
          "created_at": {
            "type": "string",
            "format": "date-time",
            "description": "Task creation timestamp"
          },
          "updated_at": {
            "type": "string",
            "format": "date-time",
            "description": "Task update timestamp"
          }
        }
      }
    },
    "pagination": {
      "type": "object",
      "properties": {
        "total": {
          "type": "integer",
          "description": "Total number of tasks"
        },
        "limit": {
          "type": "integer",
          "description": "Number of tasks per page"
        },
        "offset": {
          "type": "integer",
          "description": "Number of tasks skipped"
        },
        "has_more": {
          "type": "boolean",
          "description": "Whether more tasks are available"
        }
      }
    },
    "error": {
      "type": "string",
      "description": "Error message if operation failed"
    }
  }
}
```

### 3. update-task
Update an existing task for the authenticated user.

**Tool Name:** `update-task`

**Description:** Updates an existing task with new information for the authenticated user.

**Parameters:**
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "description": "ID of the task to update"
    },
    "title": {
      "type": "string",
      "description": "New task title (1-255 characters, optional)",
      "minLength": 1,
      "maxLength": 255
    },
    "description": {
      "type": "string",
      "description": "New task description (max 1000 characters, optional)",
      "maxLength": 1000
    },
    "completed": {
      "type": "boolean",
      "description": "New completion status (optional)"
    },
    "token": {
      "type": "string",
      "description": "JWT authentication token"
    }
  },
  "required": ["task_id", "token"]
}
```

**Result Schema:**
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the operation was successful"
    },
    "task": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique task identifier"
        },
        "title": {
          "type": "string",
          "description": "Task title"
        },
        "description": {
          "type": "string",
          "description": "Task description"
        },
        "completed": {
          "type": "boolean",
          "description": "Whether task is completed"
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "description": "Task creation timestamp"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "description": "Task update timestamp"
        }
      }
    },
    "error": {
      "type": "string",
      "description": "Error message if operation failed"
    }
  }
}
```

### 4. delete-task
Delete a task for the authenticated user.

**Tool Name:** `delete-task`

**Description:** Deletes a specific task for the authenticated user.

**Parameters:**
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "description": "ID of the task to delete"
    },
    "token": {
      "type": "string",
      "description": "JWT authentication token"
    }
  },
  "required": ["task_id", "token"]
}
```

**Result Schema:**
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the operation was successful"
    },
    "message": {
      "type": "string",
      "description": "Success message"
    },
    "error": {
      "type": "string",
      "description": "Error message if operation failed"
    }
  }
}
```

### 5. toggle-task-completion
Toggle the completion status of a task.

**Tool Name:** `toggle-task-completion`

**Description:** Toggles the completion status of a task for the authenticated user.

**Parameters:**
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "description": "ID of the task to update"
    },
    "completed": {
      "type": "boolean",
      "description": "New completion status (optional, if not provided will toggle current status)"
    },
    "token": {
      "type": "string",
      "description": "JWT authentication token"
    }
  },
  "required": ["task_id", "token"]
}
```

**Result Schema:**
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the operation was successful"
    },
    "task": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique task identifier"
        },
        "title": {
          "type": "string",
          "description": "Task title"
        },
        "description": {
          "type": "string",
          "description": "Task description"
        },
        "completed": {
          "type": "boolean",
          "description": "Whether task is completed"
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "description": "Task creation timestamp"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "description": "Task update timestamp"
        }
      }
    },
    "error": {
      "type": "string",
      "description": "Error message if operation failed"
    }
  }
}
```

### 6. get-user-profile
Get the authenticated user's profile information.

**Tool Name:** `get-user-profile`

**Description:** Retrieves the profile information of the authenticated user.

**Parameters:**
```json
{
  "type": "object",
  "properties": {
    "token": {
      "type": "string",
      "description": "JWT authentication token"
    }
  },
  "required": ["token"]
}
```

**Result Schema:**
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the operation was successful"
    },
    "user": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique user identifier"
        },
        "email": {
          "type": "string",
          "format": "email",
          "description": "User's email address"
        },
        "name": {
          "type": "string",
          "description": "User's name"
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "description": "User account creation timestamp"
        }
      }
    },
    "error": {
      "type": "string",
      "description": "Error message if operation failed"
    }
  }
}
```

### 7. process-chat-input
Process natural language input for task management.

**Tool Name:** `process-chat-input`

**Description:** Processes natural language input and executes appropriate task management actions.

**Parameters:**
```json
{
  "type": "object",
  "properties": {
    "message": {
      "type": "string",
      "description": "Natural language input from user"
    },
    "context": {
      "type": "object",
      "description": "Optional conversation context",
      "properties": {
        "conversation_id": {
          "type": "string",
          "description": "ID of the ongoing conversation"
        },
        "previous_intent": {
          "type": "string",
          "description": "Previous intent in the conversation"
        }
      }
    },
    "token": {
      "type": "string",
      "description": "JWT authentication token"
    }
  },
  "required": ["message", "token"]
}
```

**Result Schema:**
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the operation was successful"
    },
    "response": {
      "type": "string",
      "description": "AI-generated response to the user"
    },
    "action": {
      "type": "object",
      "description": "Action performed as a result of the input",
      "properties": {
        "type": "string",
        "description": "Type of action performed"
      }
    },
    "context": {
      "type": "object",
      "description": "Updated conversation context",
      "properties": {
        "conversation_id": {
          "type": "string",
          "description": "ID of the conversation"
        },
        "next_expected_input": {
          "type": "string",
          "description": "Type of input expected next"
        }
      }
    },
    "error": {
      "type": "string",
      "description": "Error message if operation failed"
    }
  }
}
```

## Error Handling

### Common Error Responses
All tools may return these standard error responses:

**401 Unauthorized:**
```json
{
  "success": false,
  "error": "Invalid or expired authentication token"
}
```

**403 Forbidden:**
```json
{
  "success": false,
  "error": "Insufficient permissions to perform this action"
}
```

**404 Not Found:**
```json
{
  "success": false,
  "error": "Requested resource not found"
}
```

**422 Unprocessable Entity:**
```json
{
  "success": false,
  "error": "Validation failed",
  "details": {
    "field": "error_description"
  }
}
```

**500 Internal Server Error:**
```json
{
  "success": false,
  "error": "Internal server error occurred"
}
```

## Security Considerations

### Authentication Validation
- All tool calls must include a valid JWT token
- Tokens must be validated for each tool invocation
- Token user ID must match the user context for the operation
- Expired tokens must be rejected

### Authorization Checks
- Users can only perform operations on their own data
- Task operations require user ID to match task owner
- Profile access limited to authenticated user's own profile

### Rate Limiting
- Tool invocations subject to rate limiting
- 50 requests per minute per authenticated user
- 100 requests per minute per IP for unauthenticated endpoints

### Input Validation
- All tool parameters must be validated
- Prevent injection attacks through proper sanitization
- Validate data types and value ranges

## Performance Requirements

### Response Times
- Tool invocation: Complete within 2 seconds
- Database operations: Complete within 1 second
- External API calls: Complete within 3 seconds

### Concurrency
- Support 100 concurrent tool invocations
- Proper database connection pooling
- Asynchronous processing where appropriate

## Implementation Guidelines

### Tool Implementation
- Each tool should be implemented as a separate function
- Follow consistent error handling patterns
- Use the same authentication middleware as REST API
- Log tool invocations for monitoring and debugging

### Data Validation
- Validate all input parameters before processing
- Use the same validation rules as REST API endpoints
- Return appropriate error messages for validation failures

### Logging and Monitoring
- Log all tool invocations with user context
- Monitor tool usage patterns and performance
- Track error rates and response times
- Implement proper audit trails for security

This specification defines the MCP tools that allow AI systems to interact with the Todo Web Application on behalf of authenticated users while maintaining security and proper authorization.