# Quickstart Guide - Todo Web Application

## Overview
This guide provides a fast path to getting the Todo Web Application up and running for development. Follow these steps to have a working development environment in minutes.

## Prerequisites
- Node.js 20+ installed
- Python 3.11+ installed
- PostgreSQL (or Docker for containerized setup)
- Git installed
- npm or yarn package manager

## Quick Setup (Using Docker - Recommended)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo-web-app
```

### 2. Copy Environment Files
```bash
# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.local.example frontend/.env.local
```

### 3. Edit Environment Variables
Update the `.env` files with your database credentials and secrets:
```bash
# In backend/.env
DATABASE_URL=postgresql://user:password@localhost:5432/todos
BETTER_AUTH_SECRET=your-super-secret-key-here-min-32-chars

# In frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

### 4. Start with Docker Compose
```bash
docker-compose up --build
```

Your application is now running:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Manual Setup (Alternative)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo-web-app
```

### 2. Set Up Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi sqlmodel psycopg2-binary pyjwt python-multipart bcrypt
pip install --dev pytest pytest-cov httpx

# Copy and edit environment file
cp .env.example .env
# Edit .env with your database URL and auth secret
```

### 3. Set Up Frontend
```bash
cd frontend

# Install dependencies
npm install

# Copy and edit environment file
cp .env.local.example .env.local
# Edit .env.local with your API URL
```

### 4. Start Both Applications
```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload

# Terminal 2: Start frontend
cd frontend
npm run dev
```

## First Steps After Setup

### 1. Register Your First User
- Navigate to http://localhost:3000/register
- Create an account with your preferred email and password

### 2. Create Your First Task
- After registration, you'll be redirected to the tasks page
- Use the "Create New Task" form to add your first task

### 3. Explore the API
- Visit http://localhost:8000/docs to explore the interactive API documentation
- Test endpoints directly from the browser

## Key Technologies Used

### Backend (Python/FastAPI)
- **FastAPI**: Modern Python web framework with automatic API docs
- **SQLModel**: SQL database modeling with Pydantic validation
- **PyJWT**: JSON Web Token implementation for authentication
- **BCrypt**: Password hashing for secure storage

### Frontend (Next.js/React)
- **Next.js 16+**: React framework with App Router
- **TypeScript**: Type-safe JavaScript development
- **Tailwind CSS**: Utility-first CSS framework
- **React Query**: Server state management and caching
- **React Hook Form**: Form validation and handling

## Common Commands

### Backend Commands
```bash
# Start development server
cd backend
uvicorn main:app --reload

# Run tests
cd backend
pytest

# Run tests with coverage
cd backend
pytest --cov=.

# Run type checking
cd backend
mypy .

# Create database tables
cd backend
python -c "from database import create_db_and_tables; create_db_and_tables()"
```

### Frontend Commands
```bash
# Start development server
cd frontend
npm run dev

# Build for production
cd frontend
npm run build

# Run tests
cd frontend
npm run test

# Run type checking
cd frontend
npm run type-check

# Lint code
cd frontend
npm run lint
```

## Project Structure
```
todo-web-app/
├── backend/                 # FastAPI backend
│   ├── main.py             # Application entry point
│   ├── models.py           # SQLModel database models
│   ├── database.py         # Database connection
│   ├── routes/             # API route definitions
│   ├── services/           # Business logic
│   ├── middleware/         # Authentication middleware
│   ├── auth.py             # JWT utilities
│   └── pyproject.toml      # Dependencies
├── frontend/               # Next.js frontend
│   ├── app/                # App Router pages
│   ├── components/         # React components
│   ├── lib/                # Utilities and API client
│   ├── hooks/              # Custom React hooks
│   ├── contexts/           # React Context providers
│   ├── package.json        # Dependencies
│   └── tsconfig.json       # TypeScript config
├── specs/                  # Specifications and documentation
│   └── 002-web-app-auth/   # Phase II specs
├── docker-compose.yml      # Docker configuration
└── README.md               # Project documentation
```

## API Endpoints Quick Reference

### Authentication
- `POST /api/auth/register` - Create new user
- `POST /api/auth/login` - User login

### Task Management
- `GET /api/tasks/{user_id}/tasks` - List user's tasks
- `POST /api/tasks/{user_id}/tasks` - Create new task
- `GET /api/tasks/{user_id}/tasks/{task_id}` - Get specific task
- `PUT /api/tasks/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/tasks/{user_id}/tasks/{task_id}/complete` - Toggle completion

## Troubleshooting Quick Fixes

### Common Issues
1. **Database Connection Error**: Verify PostgreSQL is running and credentials are correct
2. **JWT Secret Mismatch**: Ensure the same secret is used in both frontend and backend
3. **CORS Issues**: Check that frontend and backend URLs are properly configured
4. **Port Already in Use**: Change ports in docker-compose.yml or kill the process using the port

### Quick Reset
```bash
# Stop all containers
docker-compose down

# Remove volumes (warning: this will delete all data)
docker-compose down -v

# Start fresh
docker-compose up --build
```

## Development Tips

### Working with the Backend
- Use the auto-generated API documentation at `/docs`
- Leverage FastAPI's automatic validation
- Implement business logic in services, not routes
- Use dependency injection for common functionality

### Working with the Frontend
- Take advantage of React Query's caching
- Use TypeScript for better development experience
- Leverage React Hook Form for validation
- Use the App Router for page structure

### Testing
- Write tests for new functionality
- Use the existing test structure as a template
- Test both positive and negative cases
- Verify authentication and authorization flows

## Next Steps
1. Explore the API documentation at http://localhost:8000/docs
2. Review the code structure in both frontend and backend
3. Look at the specification files in `specs/002-web-app-auth/`
4. Try creating additional features following the existing patterns
5. Set up your preferred IDE with appropriate plugins for Python and TypeScript

## Getting Help
- Check the troubleshooting guide for common issues
- Review the full documentation in the `specs/` directory
- Look at the existing code patterns for guidance
- Consult the API documentation for endpoint details

This quickstart guide should have you up and running with the Todo Web Application in just a few minutes. The application is fully functional with user authentication and task management capabilities.