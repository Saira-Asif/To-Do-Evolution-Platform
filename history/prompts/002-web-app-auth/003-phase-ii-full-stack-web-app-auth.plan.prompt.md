---
id: 3
title: "Phase II Full-Stack Web App Plan"
stage: plan
date: 2026-01-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: web-app-auth
branch: "2-web-app-auth"
user: "saira"
command: "/sp.plan"
labels: ["plan", "web-app", "authentication", "full-stack"]
links:
  spec: "specs/002-web-app-auth/spec.md"
  plan: "specs/002-web-app-auth/plan.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/002-web-app-auth/plan.md"
  - "specs/002-web-app-auth/research.md"
  - "specs/002-web-app-auth/data-model.md"
  - "specs/002-web-app-auth/contracts/rest-api-contract.md"
  - "specs/002-web-app-auth/quickstart.md"
tests: []
---

# PHR: Phase II Full-Stack Web App Plan

## Prompt Text

Phase II: Full-Stack Web Application with Authentication

## Architecture Sketch
```
┌─────────────────────────────────────────────────────┐
│              Browser (User)                         │
└───────────────────┬─────────────────────────────────┘
                    │
       ┌────────────▼────────────┐
       │  Next.js Frontend       │
       │  ┌──────────────────┐   │
       │  │ Pages            │   │
       │  │ - /login           │              │
       │  ┌────────▼─────────┐   │
       │  │ SQLModel ORM     │   │
       │  └────────┬─────────┘   │
       └───────────┼─────────────┘
                   │
       ┌───────────▼─────────────┐
       │  Neon PostgreSQL dely used, manual middleware needed |
| API Structure | Flat routes / **Router-based** | Router-based | Organized, scalable, clear separation |

### Frontend Decisions
| Decision | Options | Chosen | Tradeoffs |
|----------|---------|--------|-------       │
       │  - users table          │
       │  - tasks table          │
       └─────────────────────────┘
```

## Development Approach

**Workflow:** Spec-Kit Plus structure → Write specs → Plan → Tasks → Implement via Claude Code

**Implementation Phases:**
1. **Setup (Days 1-2):** Initialize monorepo, configure Spec-Kit Plus, setup Docker Compose
2. **Backend Foundation (Days 3-4):** FastAPI app, SQLModel models, Neon DB connection
3. **Authentication (Days 5-6):** Better Auth frontend, JWT middleware backend
4. **CRUD API (Days 7-8):** Implement all 6 API endpoints with user filtering
5. **Frontend UI (Days 9-10):** Next.js pages, components, API client integration
6. **Testing & Docs (Days 11-12):** Backend tests, integration tests, documentation

**Monorepo Benefits:**
- Claude Code sees entire project in single context
- Cross-cutting changes (e.g., add field to Task) easier
- Shared types between frontend and backend
- Sing----|
| Auth Library | NextAuth / Clerk / **Better Auth** | Better Auth | JWT support, simple setup, newer library |
| State Management | Context / Zustand / **React Query** | React Query | Server state caching, optimistic updates, learning curve |
| Forms | React Hook Form / Formik / **React Hook Form** | React Hook Form | Performance, validation, TS support |
| API Client | fetch / axios / **ky** | ky | Lightweight, retry logic, better than fetch |

### Monorepo Decisions
| Decision | Options | Chosen | Tradeoffs |
|----------|---------|--------|-----------|
| Structure | Monorepo / **Monorepo** / Separate repos | Monorepo | Easier for Claude Code, single context, larger repo |
| Spec Organization | Flat / **Spec-Kit Plus** | Spec-Kit Plus | Organized, referencing, config overhead |

## Testing Strategy

### Backend Testing

**Unit Tests:**
- Test Task model validation (Pydantic)
- Test CRUD service functions
- Test JWT token generation and verification

**Integration Tests:**
- Test all API endpoints with TestClient
- Test authentication flow (signup → login → protected route)
- Test user isolation (User A cannot access User B's tasks)
- Test error cases (401, 404, 500)

**Validation Checks:**
```bash
# Run backend tests
cd backend
uv run pytest --cov=. --cov-report=term-missing

# Should achieve ≥80% coverage
# All tests should pass
```

### Frontend Testing

**Component Tests (Optional):**
- Test TaskList renders tasks correctly
- Test TaskForm validation
- Test AuthForm submission

**E2E Tests (Manual for hackathon):**
- Signup → Login → Create task → Complete task → Delete task → Logout

**Validation Checks:**
```bash
# Type checking
cd frontend
npm run type-check  # or tsc --noEmit

# Build check
npm run build  # Should build without errors
```

### Integration Testing

**Full Stack Tests:**
1. Start both services: `docker-compose up`
2. Signup new user via UI
3. Login and verify JWT token stored
4. Create 3 tasks via UI
5. Verify tasks in database: `psql $DATABASE_URL -c "SELECT * FROM tasks;"`
6. Update one task
7. Delete one task
8. Complete one task
9. Logout and verify tasks persist

**API Testing with curl:**
```bash
# Login and get token
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}' \
  | jq -r '.token')

# Get tasks
curl http://localhost:8000/api/user123/tasks \
  -H "Authorization: Bearer $TOKEN"

# Create task
curl -X POST http://localhost:8000/api/user123/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","description":"Test"}'
```

## Technical Details

### Project Setup

**Initialize Monorepo:**
```bash
mkdir phase-2-todo-web
cd phase-2-todo-web

# Create structure
mkdir -p .spec-kit specs/{features,api,database,ui} frontend backend

# Initialize Spec-Kit Plus
cat > .spec-kit/config.yaml <<EOF
name: phase-2-todo-web
version: "1.0"
structure:
  specs_dir: specs
  features_dir: specs/features
  api_dir: specs/api
  database_dir: specs/database
  ui_dir: specs/ui
phases:
  - name: phase2-web
    features: [task-crud, authentication]
EOF
```

**Backend Setup:**
```bash
cd backend
uv init
uv add fastapi sqlmodel psycopg2-binary pyjwt python-multipart
uv add --dev pytest pytest-cov httpx
```

**Frontend Setup:**
```bash
cd frontend
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir
npm install better-auth ky react-hook-form zod
```

**Docker Compose:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=todos
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"
```

### Development Workflow

1. **Write Specs:**
   - `specs/features/task-crud.md` - Feature requirements
   - `specs/api/rest-endpoints.md` - API contracts
   - `specs/database/schema.md` - Database schema
   - `specs/ui/components.md` - UI components

2. **Create CLAUDE.md Files:**
   - Root: Project overview, how to use specs
   - `frontend/CLAUDE.md`: Next.js patterns, component structure
   - `backend/CLAUDE.md`: FastAPI patterns, API conventions

3. **Implement with Claude Code:**
```
   @specs/features/task-crud.md implement backend CRUD operations
   @specs/api/rest-endpoints.md implement all 6 endpoints
   @specs/ui/components.md build TaskList component
```

4. **Test and Iterate:**
   - Run backend tests: `cd backend && uv run pytest`
   - Test frontend: `cd frontend && npm run dev`
   - Full integration: `docker-compose up`

### Code Quality Gates

**Backend:**
- [ ] All tests pass
- [ ] Coverage ≥80%
- [ ] All API endpoints return correct status codes
- [ ] JWT verification works correctly
- [ ] User isolation enforced

**Frontend:**
- [ ] TypeScript compiles with no errors
- [ ] Build succeeds: `npm run build`
- [ ] Responsive on mobile and desktop
- [ ] Forms have validation
- [ ] Loading and error states handled

**Documentation:**
- [ ] All specs updated and accurate
- [ ] CLAUDE.md files document patterns
- [ ] README has setup instructions
- [ ] API endpoints documented

### Environment Variables

**Backend (.env):**
```
DATABASE_URL=postgresql://user:pass@localhost:5432/todos
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
```

**Note:** BETTER_AUTH_SECRET must be the same in both services for JWT verification.

## Response Text

Successfully created the implementation plan for Phase II: Full-Stack Web Application with Authentication. The plan includes:

1. Technical Context - Architecture overview and current/target state
2. Constitution Check - Compliance with project principles
3. Implementation Phases - Detailed breakdown of work across 5 phases:
   - Phase 0: Project Setup (Days 1-2)
   - Phase 1: Authentication System (Days 3-4)
   - Phase 2: Core API Development (Days 5-6)
   - Phase 3: Frontend UI Development (Days 7-8)
   - Phase 4: Testing and Quality Assurance (Days 9-10)
   - Phase 5: Documentation and Deployment (Days 11-12)
4. Risk Assessment and Mitigation - Identified high-risk areas
5. Success Criteria - Functional and non-functional requirements
6. Resource Requirements - Development environment and external services
7. Timeline and Milestones - Week-by-week breakdown
8. Validation Checklist - Criteria for phase completion

Also created supporting documents:
- research.md: Technology decisions and rationale
- data-model.md: Entity models and API DTOs
- contracts/rest-api-contract.md: Detailed API contract
- quickstart.md: Quick setup and usage guide

All artifacts are properly organized in the specs/002-web-app-auth/ directory structure.

## Outcome

The implementation plan is complete and ready for the next phase of development. The plan provides a clear roadmap for implementing the full-stack web application with authentication, with proper attention to security, scalability, and maintainability requirements. All supporting documentation has been created to guide the implementation process.