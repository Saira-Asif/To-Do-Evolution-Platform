# Database Schema Specification

## Overview
The Todo Web Application uses PostgreSQL as its primary database with SQLModel as the ORM. The schema is designed to support user authentication and task management with proper relationships and constraints.

## Database Configuration
- **Database**: PostgreSQL (hosted on Neon DB)
- **ORM**: SQLModel (SQLAlchemy + Pydantic integration)
- **Connection Pooling**: Managed by SQLModel/SQLAlchemy
- **Migration Tool**: Alembic for schema migrations

## Table Schema

### 1. users Table
Stores user account information for authentication and identification.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**
- `id`: Primary key, UUID, auto-generated unique identifier
- `email`: VARCHAR(255), unique, not null, user's email address
- `name`: VARCHAR(100), optional, user's display name
- `password_hash`: VARCHAR(255), not null, BCrypt hash of user's password
- `created_at`: Timestamp with timezone, default current timestamp
- `updated_at`: Timestamp with timezone, default current timestamp, updated on modification

**Constraints:**
- Primary Key: id
- Unique Constraint: email
- Not Null: id, email, password_hash, created_at, updated_at

**Indexes:**
- Primary Key Index: id (automatic)
- Unique Index: email
- Regular Index: created_at (for ordering and filtering)

**Triggers:**
- `update_updated_at_trigger`: Automatically updates `updated_at` field on row modification

### 2. tasks Table
Stores user tasks with relationship to the users table.

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Fields:**
- `id`: Primary key, UUID, auto-generated unique identifier
- `user_id`: UUID, foreign key to users table, not null
- `title`: VARCHAR(255), not null, task title
- `description`: TEXT, optional, task description
- `completed`: BOOLEAN, default false, completion status
- `created_at`: Timestamp with timezone, default current timestamp
- `updated_at`: Timestamp with timezone, default current timestamp, updated on modification

**Constraints:**
- Primary Key: id
- Foreign Key: user_id references users(id) with cascade delete
- Not Null: id, user_id, title, created_at, updated_at
- Check: title length between 1 and 255 characters

**Indexes:**
- Primary Key Index: id (automatic)
- Foreign Key Index: user_id (for join operations)
- Index: completed (for filtering completed/pending tasks)
- Index: created_at (for ordering and filtering)
- Composite Index: (user_id, completed) for common queries

**Triggers:**
- `update_updated_at_trigger`: Automatically updates `updated_at` field on row modification

## SQLModel Definitions

### User Model
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    name: Optional[str] = Field(default=None, max_length=100)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")
```

### Task Model
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(nullable=False, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", ondelete="CASCADE")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationship to user
    user: User = Relationship(back_populates="tasks")
```

## Indexing Strategy

### Primary Indexes
- All primary keys are automatically indexed by PostgreSQL

### Secondary Indexes
- `users.email`: Unique index for fast email lookups during authentication
- `users.created_at`: Index for ordering users by creation date
- `tasks.user_id`: Index for fast user-task relationship queries
- `tasks.completed`: Index for filtering completed vs pending tasks
- `tasks.created_at`: Index for ordering tasks by creation date
- `tasks.updated_at`: Index for ordering tasks by update date

### Composite Indexes
- `(tasks.user_id, tasks.completed)`: For common queries filtering tasks by user and completion status
- `(tasks.user_id, tasks.created_at)`: For ordered task lists per user

## Relationships

### User-Task Relationship
- **Type**: One-to-Many (One user to many tasks)
- **Foreign Key**: `tasks.user_id` references `users.id`
- **Cascade**: DELETE CASCADE - when a user is deleted, all their tasks are automatically deleted
- **Constraint**: Not null on `tasks.user_id` ensures every task belongs to a user

## Data Integrity Constraints

### Check Constraints
- Task title length: 1-255 characters
- User email format: Valid email format validation at application level
- Password hash: Non-empty validation at application level

### Referential Integrity
- Foreign key constraint ensures tasks always reference valid users
- CASCADE delete ensures data consistency when users are removed

## Security Considerations

### Data Protection
- Passwords stored as BCrypt hashes, never in plain text
- User emails are unique to prevent account conflicts
- Proper access controls ensure users can only access their own data

### Access Patterns
- All queries filtered by user_id to ensure data isolation
- Authentication required for all data access operations
- Audit trails for sensitive operations (future enhancement)

## Performance Considerations

### Query Optimization
- Proper indexing for common query patterns
- Efficient foreign key relationships for joins
- Pagination support for large datasets

### Connection Management
- Connection pooling to optimize database connections
- Asynchronous operations to handle concurrent requests
- Prepared statements for frequently executed queries

## Migration Strategy

### Initial Schema
- Create users table with all required fields and constraints
- Create tasks table with proper foreign key relationship
- Create all necessary indexes
- Set up triggers for automatic timestamp updates

### Future Migrations
- Use Alembic for schema evolution
- Maintain backward compatibility during migrations
- Test migrations in staging environment before production

## Backup and Recovery

### Backup Strategy
- Automated daily backups of PostgreSQL database
- Point-in-time recovery capabilities
- Off-site backup storage for disaster recovery

### Recovery Procedures
- Documented recovery procedures for different failure scenarios
- Regular backup testing to ensure data integrity
- Rollback procedures for failed migrations

## Monitoring and Maintenance

### Schema Monitoring
- Monitor for performance degradation due to schema changes
- Track query performance against indexes
- Monitor database connection pool usage

### Maintenance Tasks
- Regular vacuum and analyze operations
- Index optimization based on usage patterns
- Archive old data that is no longer frequently accessed (future enhancement)

This database schema provides a solid foundation for the Todo Web Application with proper relationships, constraints, and performance considerations.