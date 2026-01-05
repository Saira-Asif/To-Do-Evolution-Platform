---
id: 2
title: "Phase II Full-Stack Web App Auth Spec"
stage: spec
date: 2026-01-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: web-app-auth
branch: "2-web-app-auth"
user: "saira"
command: "/sp.specify"
labels: ["spec", "web-app", "authentication", "full-stack"]
links:
  spec: "specs/002-web-app-auth/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/002-web-app-auth/spec.md"
  - "specs/002-web-app-auth/checklists/requirements.md"
tests: []
---

# PHR: Phase II Full-Stack Web App Auth Spec

## Prompt Text

Phase II: Full-Stack Web Application with Authentication

**Target audience:** Full-stack developers building secure multi-user web applications with spec-driven development
**Focus:** Transform Phase I console app into a production-ready web application with persistent storage and user authentication

## Success Criteria

**Basic Level Features (Required - 5/5):**
- Create task via web form with title and description
- View all tasks in responsive web interface with status indicators
- Update task details through edit form
- Delete tasks with confirmation
- Mark tasks as complete/incomplete with toggle

**Multi-User & Authentication:**
- User signup/signin using Better Auth
- JWT token-based API authentication
- User isolation - each user sees only their own tasks
- Protected API routes requiring valid JWT tokens

**Technical Requirements:**
- RESTful API with 6 endpoints (GET, POST, GET by ID, PUT, DELETE, PATCH)
- Responsive frontend works on mobile and desktop
- Data persists in Neon PostgreSQL database
- All API requests filtered by authenticated user_id
- Monorepo structure with frontend/ and backend/ folders

**Code Quality:**
- No manual coding - all implementation via Claude Code
- 80%+ test coverage (backend API tests)
- Type-safe API client on frontend
- Proper error handling (401 Unauthorized, 404 Not Found, etc.)

**Documentation:**
- Spec-Kit Plus organized specs folder structure
- Root CLAUDE.md + frontend/CLAUDE.md + backend/CLAUDE.md
- README.md with setup instructions for both services
- API documentation in specs/api/rest-endpoints.md

## Constraints

**Technology Stack:**
- **Frontend:** Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend:** Python FastAPI, SQLModel ORM
- **Database:** Neon Serverless PostgreSQL
- **Authentication:** Better Auth with JWT tokens
- **Development:** Claude Code + Spec-Kit Plus
- **Deployment:** Docker Compose for local development

**Monorepo Structure:**
```
phase-2-todo-web/
├── .spec-kit/
│   └── config.yaml
├── specs/
│   ├── overview.md
│   ├── architecture.md
│   ├── features/
│   │   ├── task-crud.md
│   │   └── authentication.md
│   ├── api/
│   │   └── rest-endpoints.md
│   ├── database/
│   │   └── schema.md
│   └── ui/
│       ├── components.md
│       └── pages.md
├── frontend/
│   ├── CLAUDE.md
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── package.json
├── backend/
│   ├── CLAUDE.md
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   └── pyproject.toml
├── docker-compose.yml
├── CLAUDE.md
└── README.md
```

**API Endpoints:**
- `GET /api/{user_id}/tasks` - List all user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get task details
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

**Security Requirements:**
- JWT tokens issued by Better Auth on login
- All API requests include `Authorization: Bearer <token>` header
- Backend verifies t
- Clear commit messages showing AI-generated iterationsJWT signature using shared secret
- User_id in URL must match user_id in JWT token
- Return 401 Unauthorized for invalid/missing tokens

**Database Schema:**
```
users (managed by Better Auth):
- id: string (PK)
- email: string (unique)
- name: string
- created_at: timestamp

tasks:
- id: integer (PK)
- user_id: string (FK -> users.id)
- title: string (not null, max 200 chars)
- description: text (nullable, max 1000 chars)
- completed: boolean (default false)
- created_at: timestamp
- updated_at: timestamp
```

**Timeline:** Complete by December 14, 2025

## Not Building (Out of Scope)

**Phase I Features (Already Built):**
- ❌ Console CLI interface (Phase I complete)

**Intermediate/Advanced Features (Future):**
- ❌ Priorities, tags, categories
- ❌ Search, filter, sort (beyond basic status filter)
- ❌ Due dates and reminders
- ❌ Recurring tasks
- ❌ AI chatbot (Phase III)
- ❌ File attachments
- ❌ Email notifications
- ❌ Team collaboration/sharing
- ❌ Task comments or activity history
- ❌ Keyboard shortcuts

**Authentication Features:**
- ❌ OAuth providers (Google, GitHub) - use email/password only
- ❌ Multi-factor authentication
- ❌ Password reset via email (optional nice-to-have)
- ❌ Admin roles or permissions

**Deployment:**
- ❌ Production cloud deployment (Phase V)
- ❌ Kubernetes (Phase IV)
- ❌ CI/CD pipelines

## Detailed Scope

**Frontend Pages:**
1. **Login Page** (`/login`) - Email/password form with Better Auth
2. **Signup Page** (`/signup`) - User registration
3. **Tasks Dashboard** (`/tasks`) - Protected route showing user's tasks
4. **Create Task** - Modal or inline form
5. **Edit Task** - Modal or inline form

**Frontend Components:**
- `TaskList` - Display all tasks with status indicators
- `TaskItem` - Single task with edit/delete/complete actions
- `TaskForm` - Create/edit task form with validation
- `AuthForm` - Reusable login/signup form
- Navigation with user info and logout

**Backend Structure:**
- `main.py` - FastAPI app, CORS, JWT middleware
- `models.py` - SQLModel User and Task models
- `routes/auth.py` - Better Auth integration endpoints (if needed)
- `routes/tasks.py` - CRUD endpoints for tasks
- `db.py` - Database connection and session management
- `auth.py` - JWT verification middleware

**Better Auth + FastAPI Integration:**
1. Better Auth (frontend) issues JWT tokens on login
2. Frontend stores token (httpOnly cookie or localStorage)
3. Frontend includes token in all API requests
4. Backend middleware extracts and verifies token
5. Backend matches user_id in URL with token user_id
6. Backend filters all queries by authenticated user

**Validation Rules:**
- Title: Required, 1-200 characters
- Description: Optional, max 1000 characters
- User must own task to update/delete
- Completed: Boolean toggle only

## Validation Criteria

**Functional:**
- User can signup, login, and logout
- User can perform all 5 CRUD operations via web UI
- Tasks persist across sessions in PostgreSQL
- User A cannot see User B's tasks
- Invalid tokens return 401 Unauthorize

## Response Text

Created a comprehensive specification for the Phase II Full-Stack Web Application with Authentication feature. The spec includes:

- Feature overview with business value
- Clear scope definition (in-scope and out-of-scope)
- User scenarios and acceptance criteria
- Detailed functional requirements (authentication, task management, data, API)
- Non-functional requirements (performance, security, usability)
- Measurable success criteria (quantitative and qualitative)
- Key entities (User, Task, Authentication Token)
- Assumptions and dependencies
- Technology and timeline constraints

Also created a quality checklist to validate the specification completeness. The specification is ready for the planning phase.

## Outcome

Successfully created feature specification for Phase II web application with authentication. The spec is comprehensive, testable, and ready for planning phase. All requirements are clearly defined with measurable success criteria.