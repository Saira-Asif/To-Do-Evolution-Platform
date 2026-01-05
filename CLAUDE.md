# Todo Web Application - Claude Code Instructions

## Overview
This is a full-stack web application with authentication for managing tasks. The application consists of a Next.js frontend and a FastAPI backend with PostgreSQL database.

## Project Structure
- `frontend/` - Next.js application with TypeScript and Tailwind CSS
- `backend/` - FastAPI application with SQLModel ORM
- `specs/` - Specification, plan, and task files for each feature
- `history/` - History of prompts and ADRs

## Development Workflow
1. Follow the Spec-Kit Plus methodology with specifications, plans, and tasks
2. Implement features in the order specified in the tasks.md files
3. Use Claude Code for AI-assisted development
4. Maintain clean architecture with separation of concerns

## Technology Stack
- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS, React Query, React Hook Form
- **Backend**: FastAPI, Python 3.11+, SQLModel, Pydantic
- **Database**: PostgreSQL (Neon DB)
- **Authentication**: Better Auth with JWT tokens

## Key Patterns
- Use Next.js App Router for frontend routing
- Implement FastAPI with async/await patterns
- Use SQLModel for database models with Pydantic validation
- Follow RESTful API design principles
- Implement proper error handling and validation

## Common Commands
- `cd backend && uvicorn main:app --reload` - Start backend server
- `cd frontend && npm run dev` - Start frontend server
- `cd backend && pytest` - Run backend tests
- `cd frontend && npm run type-check` - Check TypeScript types

## Architecture Notes
- User ID is passed in URL path for authentication context
- JWT tokens are validated for each request
- All database queries are filtered by authenticated user
- API responses follow consistent format with proper HTTP status codes