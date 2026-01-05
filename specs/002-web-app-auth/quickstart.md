# Quickstart Guide - Phase II: Full-Stack Web Application with Authentication

## Overview
This guide provides a quick introduction to setting up and running the Full-Stack Web Application with Authentication. The application consists of a Next.js frontend and a FastAPI backend with PostgreSQL database.

## Prerequisites
- Node.js 20+ (for frontend development)
- Python 3.11+ (for backend development)
- PostgreSQL-compatible database (Neon DB recommended)
- Docker and Docker Compose (for containerized deployment)
- Git

## Architecture Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (Next.js)     │───▶│   (FastAPI)     │───▶│ (PostgreSQL)    │
│                 │    │                 │    │                 │
│  - React        │    │  - SQLModel     │    │  - Users table  │
│  - TypeScript   │    │  - Pydantic     │    │  - Tasks table  │
│  - Tailwind CSS │    │  - JWT Auth     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Local Development Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd phase-2-todo-web
```

### 2. Set Up Backend
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi sqlmodel psycopg2-binary pyjwt python-multipart
pip install --dev pytest pytest-cov httpx

# Set environment variables
cp .env.example .env
# Edit .env with your database URL and auth secret
```

### 3. Set Up Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# Or with yarn: yarn install

# Set environment variables
cp .env.local.example .env.local
# Edit .env.local with your API URL and auth settings
```

### 4. Database Setup
```bash
# Make sure PostgreSQL is running
# Create the database tables using the backend
cd backend
python -c "from database import create_db_and_tables; create_db_and_tables()"
```

### 5. Run Applications
```bash
# Terminal 1: Start backend
cd backend
uvicorn main:app --reload

# Terminal 2: Start frontend
cd frontend
npm run dev
```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/todos
BETTER_AUTH_SECRET=your-super-secret-key-here-min-32-chars
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

## API Endpoints Overview

### Authentication Endpoints (via Better Auth)
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Task Management Endpoints
- `GET /api/{user_id}/tasks` - List user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Basic Usage Flow

1. **Register**: Create an account at `/register`
2. **Login**: Sign in at `/login`
3. **Create Tasks**: Use the form to add new tasks
4. **View Tasks**: See all your tasks on the dashboard
5. **Update Tasks**: Edit existing tasks
6. **Complete Tasks**: Mark tasks as done
7. **Delete Tasks**: Remove completed tasks

## Running with Docker Compose
```bash
# From project root
docker-compose up --build

# Services will be available at:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Database: http://localhost:5432
```

## Testing
```bash
# Backend tests
cd backend
pytest --cov=.

# Frontend tests
cd frontend
npm run test

# Type checking
npm run type-check
```

## Key Technologies

### Backend
- **FastAPI**: Modern Python web framework with automatic API docs
- **SQLModel**: SQL database modeling with Pydantic validation
- **PyJWT**: JSON Web Token implementation for authentication
- **PostgreSQL**: Relational database for data persistence

### Frontend
- **Next.js 16+**: React framework with App Router
- **TypeScript**: Type-safe JavaScript development
- **Tailwind CSS**: Utility-first CSS framework
- **React Query**: Server state management and caching
- **React Hook Form**: Form validation and handling
- **ky**: Lightweight HTTP client

### Authentication
- **Better Auth**: Modern authentication library with JWT support

## Troubleshooting

### Common Issues
1. **Database Connection**: Ensure PostgreSQL is running and credentials are correct
2. **JWT Secret**: Make sure the same secret is used in both frontend and backend
3. **CORS Issues**: Check that frontend and backend URLs are properly configured
4. **Environment Variables**: Verify all required environment variables are set

### API Testing
```bash
# Test authentication
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# Test task creation (with valid token)
curl -X POST http://localhost:8000/api/user123/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","description":"Test description"}'
```

## Next Steps
1. Explore the API documentation at `http://localhost:8000/docs`
2. Review the database schema in `backend/models.py`
3. Check the frontend components in `frontend/app/components/`
4. Look at the API contract in `specs/002-web-app-auth/contracts/`