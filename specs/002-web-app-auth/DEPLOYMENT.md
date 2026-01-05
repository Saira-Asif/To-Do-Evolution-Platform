# Deployment Guide - Todo Web Application

## Overview
This guide provides instructions for deploying the Todo Web Application to different environments, from local development to production.

## Prerequisites

### Local Development
- Node.js 20+ (for frontend)
- Python 3.11+ (for backend)
- PostgreSQL-compatible database
- Docker and Docker Compose (optional, for containerized deployment)

### Production Deployment
- Server with Docker and Docker Compose installed
- Reverse proxy (nginx, Apache, etc.) for SSL termination
- Domain name pointing to server IP
- SSL certificate (Let's Encrypt or purchased)

## Local Development Deployment

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo-web-app
```

### 2. Set Up Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/todos
BETTER_AUTH_SECRET=your-super-secret-key-here-min-32-chars
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

### 3. Run with Docker Compose (Recommended)
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Database: http://localhost:5432

### 4. Run Manually (Alternative)
```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload

# Terminal 2: Start frontend
cd frontend
npm run dev
```

## Production Deployment

### 1. Prepare Production Environment
```bash
# Create production directories
sudo mkdir -p /opt/todo-app/{frontend,backend}
sudo chown -R $USER:$USER /opt/todo-app
```

### 2. Set Up Production Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@prod-db:5432/todos
BETTER_AUTH_SECRET=your-production-secret-key-at-least-32-chars
LOG_LEVEL=INFO
PORT=8000
```

#### Frontend (.env)
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_BETTER_AUTH_URL=https://yourdomain.com
```

### 3. Build Docker Images
```bash
# Build production images
docker build -t todo-frontend:latest -f Dockerfile.frontend .
docker build -t todo-backend:latest -f Dockerfile.backend .
docker build -t todo-db:latest -f Dockerfile.db .
```

### 4. Deploy with Docker Compose
Create a production docker-compose.yml:
```yaml
version: '3.8'
services:
  backend:
    image: todo-backend:latest
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - LOG_LEVEL=INFO
    ports:
      - "8000:8000"
    depends_on:
      - db
    restart: unless-stopped

  frontend:
    image: todo-frontend:latest
    environment:
      - NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
    ports:
      - "3000:3000"
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=todos
      - POSTGRES_USER=todo_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

volumes:
  postgres_data:
```

Deploy:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 5. Set Up Reverse Proxy (nginx)
Configure nginx to serve the frontend and proxy API requests:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    # Serve frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Proxy API requests to backend
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Environment-Specific Configuration

### Development
- Use SQLite or local PostgreSQL for development
- Enable debug mode and hot reloading
- Use less restrictive CORS settings
- Detailed error messages

### Staging
- Use separate database instance
- Monitor application performance
- Test deployment process
- Limited access for testing

### Production
- Use production-grade database cluster
- Enable caching and CDN
- Strict security settings
- Comprehensive monitoring and alerting

## Database Migration
When deploying updates that include database schema changes:

```bash
# Run database migrations
cd backend
python -c "from database import create_db_and_tables; create_db_and_tables()"
```

## Security Best Practices

### HTTPS
- Always use HTTPS in production
- Implement HSTS headers
- Use strong cipher suites

### Environment Variables
- Never commit secrets to version control
- Use different secrets for each environment
- Rotate secrets periodically

### Rate Limiting
- Implement rate limiting on authentication endpoints
- Consider DDoS protection
- Monitor for unusual traffic patterns

## Monitoring and Logging

### Application Logs
- Structured logging for easy parsing
- Log to stdout/stderr for containerized deployments
- Centralized log aggregation

### Health Checks
- Implement health check endpoints
- Monitor response times
- Set up alerts for failures

### Performance Monitoring
- Track API response times
- Monitor database performance
- Watch resource utilization

## Rollback Strategy

### Blue-Green Deployment
1. Deploy new version to staging environment
2. Test functionality
3. Switch traffic to new version
4. Keep old version running until verified
5. Decommission old version if successful

### Rollback Process
1. Switch traffic back to old version
2. Investigate and fix issues
3. Redeploy corrected version

## Troubleshooting

### Common Issues

#### Database Connection
- Verify database URL is correct
- Check database credentials
- Ensure database service is running

#### Authentication Failures
- Verify JWT secret is consistent
- Check that CORS settings allow frontend domain
- Ensure proper HTTPS configuration

#### Application Performance
- Monitor database query performance
- Implement caching where appropriate
- Scale resources as needed

### Debugging Production Issues
1. Check application logs
2. Verify environment variables
3. Test database connectivity
4. Monitor resource usage
5. Review recent changes

## Maintenance Tasks

### Regular Maintenance
- Update dependencies regularly
- Rotate secrets periodically
- Clean up old logs
- Monitor disk space

### Backup Strategy
- Regular database backups
- Secure backup storage
- Test backup restoration process
- Encrypt backups in transit and at rest

This deployment guide covers the essential steps for deploying the Todo Web Application in various environments. Always test deployment procedures in a staging environment before applying to production.