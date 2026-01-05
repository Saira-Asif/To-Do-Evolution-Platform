# Troubleshooting Guide - Todo Web Application

## Overview
This guide provides solutions to common issues encountered during development, testing, and deployment of the Todo Web Application.

## Common Issues and Solutions

### Database Connection Issues

#### Issue: Cannot connect to PostgreSQL database
**Symptoms:**
- `Connection refused` error
- `FATAL: password authentication failed`
- `database "todos" does not exist`

**Solutions:**
1. **Verify database service is running:**
   ```bash
   # Check if PostgreSQL is running
   sudo systemctl status postgresql

   # Start PostgreSQL if not running
   sudo systemctl start postgresql
   ```

2. **Check database credentials in `.env`:**
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/todos
   ```

3. **Create the database if it doesn't exist:**
   ```bash
   # Connect to PostgreSQL as superuser
   psql -U postgres

   # Create the database
   CREATE DATABASE todos;
   CREATE USER todo_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE todos TO todo_user;
   ```

#### Issue: Migration problems
**Symptoms:**
- `relation does not exist` errors
- `column does not exist` errors

**Solutions:**
1. **Recreate database tables:**
   ```bash
   cd backend
   python -c "from database import create_db_and_tables; create_db_and_tables()"
   ```

2. **Check that your models match the database schema:**
   - Verify that all model fields exist in the database
   - Check for typos in field names

### Authentication Issues

#### Issue: JWT token validation failures
**Symptoms:**
- `Could not validate credentials` error
- `Signature verification failed` error
- `Expired token` error

**Solutions:**
1. **Verify that `BETTER_AUTH_SECRET` is the same in both frontend and backend:**
   ```env
   # Backend .env
   BETTER_AUTH_SECRET=your-super-secret-key-here-min-32-chars

   # Frontend .env.local (should match)
   NEXT_PUBLIC_BETTER_AUTH_SECRET=your-super-secret-key-here-min-32-chars
   ```

2. **Check that the secret is at least 32 characters long:**
   ```bash
   # Generate a new secret if needed
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Verify token expiration settings:**
   - Check `ACCESS_TOKEN_EXPIRE_MINUTES` in `auth.py`
   - Adjust as needed for your use case

#### Issue: User cannot register/login
**Symptoms:**
- Registration returns 400 error
- Login returns "Incorrect email or password"
- No error messages provided

**Solutions:**
1. **Check the request format:**
   - Verify JSON structure
   - Ensure all required fields are provided
   - Check that passwords meet requirements (8+ characters)

2. **Verify that the user doesn't already exist:**
   - Check for duplicate email addresses
   - Ensure unique constraint on email field

3. **Debug authentication service:**
   ```bash
   # Test registration endpoint directly
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"password123","name":"Test User"}'
   ```

### Frontend Issues

#### Issue: API calls returning 401 Unauthorized
**Symptoms:**
- All API requests fail with 401
- Token exists in localStorage but still fails
- CORS errors in browser console

**Solutions:**
1. **Verify token is properly stored and sent:**
   - Check localStorage for auth token: `localStorage.getItem('auth_token')`
   - Verify Authorization header format: `Authorization: Bearer <token>`

2. **Check CORS configuration:**
   ```python
   # In main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],  # Match your frontend URL
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. **Ensure proper token refresh:**
   - Check that expired tokens are handled correctly
   - Implement token refresh logic if needed

#### Issue: React Query not updating after mutations
**Symptoms:**
- Data doesn't update after create/update/delete operations
- Need to refresh page to see changes
- Stale data displayed

**Solutions:**
1. **Verify that queries are invalidated properly:**
   ```javascript
   // In mutation success handlers
   onSuccess: () => {
     queryClient.invalidateQueries(['tasks']); // Ensure correct query key
   }
   ```

2. **Check React Query configuration:**
   ```javascript
   // Ensure proper configuration
   const queryClient = new QueryClient({
     defaultOptions: {
       queries: {
         staleTime: 5 * 60 * 1000, // 5 minutes
         retry: 1,
       },
     },
   });
   ```

### Backend Issues

#### Issue: FastAPI endpoints not working
**Symptoms:**
- Endpoints return 404 Not Found
- API documentation at `/docs` not accessible
- Routes not registering properly

**Solutions:**
1. **Verify route registration in `main.py`:**
   ```python
   # Ensure all routers are included
   app.include_router(auth.router, prefix="/api")
   app.include_router(tasks.router, prefix="/api")
   ```

2. **Check for import errors:**
   - Verify that route files are properly imported
   - Check for circular imports
   - Ensure all dependencies are installed

3. **Debug with uvicorn:**
   ```bash
   # Run with debug output
   uvicorn main:app --reload --log-level debug
   ```

#### Issue: SQLModel validation errors
**Symptoms:**
- `ValidationError` when creating models
- Field validation failing unexpectedly
- Type conversion issues

**Solutions:**
1. **Check field definitions in models:**
   ```python
   # Verify field constraints
   title: str = Field(min_length=1, max_length=200)
   description: Optional[str] = Field(default=None, max_length=1000)
   ```

2. **Validate input data:**
   - Ensure data types match model definitions
   - Check for null values in non-nullable fields
   - Verify field lengths match constraints

### Docker Issues

#### Issue: Container fails to start
**Symptoms:**
- Container exits immediately after starting
- Error messages during `docker-compose up`
- Port binding failures

**Solutions:**
1. **Check container logs:**
   ```bash
   docker-compose logs <service-name>
   docker logs <container-id>
   ```

2. **Verify environment variables:**
   - Ensure all required environment variables are set
   - Check for special characters that need escaping

3. **Test individual containers:**
   ```bash
   # Run a single service to isolate issues
   docker-compose up backend
   ```

#### Issue: Database container won't start
**Symptoms:**
- Database container keeps restarting
- Volume permission errors
- Initialization script failures

**Solutions:**
1. **Check database logs:**
   ```bash
   docker-compose logs db
   ```

2. **Reset database volume (WARNING: This will lose data):**
   ```bash
   docker-compose down -v
   docker-compose up db
   ```

3. **Verify volume permissions:**
   ```bash
   # Ensure proper ownership of volume directory
   sudo chown -R 999:999 /path/to/db/volume
   ```

## Performance Issues

### Slow API Response Times
**Causes and Solutions:**
1. **Database queries not optimized:**
   - Add indexes to frequently queried fields
   - Use proper JOINs instead of multiple queries
   - Implement pagination for large result sets

2. **Missing database indexes:**
   ```sql
   -- Add index for user_id in tasks table
   CREATE INDEX idx_tasks_user_id ON tasks(user_id);
   ```

3. **N+1 query problems:**
   - Use eager loading where appropriate
   - Batch queries instead of individual lookups

### High Memory Usage
**Causes and Solutions:**
1. **Large result sets loaded into memory:**
   - Implement pagination
   - Use streaming responses for large datasets
   - Optimize queries to return only needed fields

2. **Memory leaks:**
   - Check for unclosed database connections
   - Verify proper resource cleanup
   - Monitor for circular references

## Security Issues

### JWT Token Compromise
**Prevention:**
1. **Use strong secrets:**
   - At least 32 characters
   - Randomly generated
   - Different for each environment

2. **Short token expiration:**
   - Set appropriate expiration times
   - Implement refresh token mechanism

3. **Secure token storage:**
   - Use httpOnly cookies in production
   - Implement proper XSS protection

### SQL Injection Prevention
**Best Practices:**
1. **Always use parameterized queries:**
   - SQLModel handles this automatically
   - Never concatenate user input directly into queries

2. **Input validation:**
   - Validate all inputs before database operations
   - Use Pydantic models for request validation

## Debugging Strategies

### Enable Detailed Logging
1. **Backend logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Frontend debugging:**
   - Enable React Developer Tools
   - Use console.log statements strategically
   - Check network tab for API request details

### API Testing
1. **Use tools like curl or Postman:**
   ```bash
   curl -X GET http://localhost:8000/api/tasks/user123/tasks \
     -H "Authorization: Bearer your-token-here"
   ```

2. **Test endpoints individually:**
   - Verify each endpoint works in isolation
   - Check request/response formats
   - Validate error handling

## Deployment-Specific Issues

### Production Deployment Problems
1. **Check file permissions:**
   ```bash
   # Ensure correct permissions for production
   sudo chown -R appuser:appuser /opt/todo-app
   ```

2. **Verify environment configuration:**
   - Check that production variables are set
   - Ensure database connection is available
   - Verify SSL certificates are valid

3. **Monitor resource limits:**
   - Check memory and CPU usage
   - Verify disk space availability
   - Monitor application logs for errors

## Getting Help

### When to Contact Support
Contact support for:
- Persistent database connection issues
- Security vulnerabilities
- Performance problems in production
- Deployment failures

### Useful Commands for Debugging
```bash
# Check all running containers
docker ps

# View application logs
docker-compose logs --tail=50 -f

# Check network connectivity
docker exec -it <container> ping <other-container>

# Access container shell
docker exec -it <container> sh

# Run tests to verify functionality
cd backend && pytest
cd frontend && npm test
```

This troubleshooting guide covers the most common issues encountered with the Todo Web Application. If you encounter an issue not covered here, check the application logs and verify that all configuration settings match your environment.