---
id: 5
title: "Phase II Arch Decisions ADR"
stage: refactor
date: 2026-01-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: web-app-auth
branch: "2-web-app-auth"
user: "saira"
command: "/sp.adr"
labels: ["adr", "architecture", "web-app", "authentication"]
links:
  spec: "specs/002-web-app-auth/spec.md"
  plan: "specs/002-web-app-auth/plan.md"
  tasks: "specs/002-web-app-auth/tasks.md"
  ticket: null
  adr: null
  pr: null
files:
  - "history/adr/005-monorepo-structure.md"
  - "history/adr/006-better-auth.md"
  - "history/adr/007-jwt-storage.md"
  - "history/adr/008-sqlmodel-orm.md"
  - "history/adr/009-user-id-in-path.md"
  - "history/adr/010-neon-postgresql.md"
  - "history/adr/011-spec-kit-plus-structure.md"
tests: []
---

# PHR: Phase II Arch Decisions ADR

## Prompt Text

Phase II: Full-Stack Web Application with Authentication

Review the generated plan and record key Architectural Decisions for Phase II.

Focus on decisions that:
1. Affect the integration between frontend and backend
2. Had viable alternatives with significant tradeoffs
3. Will impact Phase III (AI chatbot integration)
4. Reviewers or judges will want to understand

**Phase II Specific ADR-Worthy Decisions:**
- Monorepo vs separate repos for frontend/backend
- Better Auth vs NextAuth vs Clerk for authentication
- JWT storage location (cookie vs localStorage vs sessionStorage)
- SQLModel vs SQLAlchemy vs Prisma for ORM
- API authentication strategy (JWT in header vs cookie)
- User ID in URL path vs query param vs JWT-only
- Neon PostgreSQL vs other database providers
- Spec-Kit Plus organization structure

**Not ADR-Worthy for Phase II:**
- Using Next.js 16+ (hackathon requirement)
- Using FastAPI (hackathon requirement)
- Using Tailwind CSS (standard choice)
- HTTP status codes (standard REST practice)

**ADR Structure:**
```
# ADR-00X: [Decision Title]

## Status
Accepted

## Context
[Why was this decision needed? What problem or requirement drove it?]

## Decision
[What did we choose?]

## Alternatives Considered
1. **Option A**:
   - Pro: ...
   - Con: ...
   - Impact on Phase III: ...

2. **Option B**:
   - Pro: ...
   - Con: ...
   - Impact on Phase III: ...

3. **Option C** (Chosen):
   - Pro: ...
   - Con: ...
   - Impact on Phase III: ...

## Rationale
[Why this choice over alternatives? Consider: developer experience, security, scalability, Phase III requirements]

## Consequences
- Positive: [Benefits]
- Negative: [Tradeoffs]
- Impact on Phase III: [Migration considerations]
```

## Response Text

Successfully created 7 Architectural Decision Records (ADRs) for Phase II: Full-Stack Web Application with Authentication:

1. **ADR-005: Monorepo Structure for Full-Stack Application** - Decision to use monorepo structure with both frontend and backend in a single repository
2. **ADR-006: Better Auth for Authentication System** - Decision to use Better Auth for the authentication system
3. **ADR-007: JWT Token Storage in Browser** - Decision to store JWT tokens in localStorage for the frontend application
4. **ADR-008: SQLModel for Database ORM** - Decision to use SQLModel as the ORM for database operations
5. **ADR-009: User ID in URL Path for API Endpoints** - Decision to include user_id as a path parameter in API endpoints
6. **ADR-010: Neon PostgreSQL for Database Provider** - Decision to use Neon Serverless PostgreSQL as the database provider
7. **ADR-011: Spec-Kit Plus Organization Structure** - Decision to use the Spec-Kit Plus structure with organized specs/ directory

All ADRs follow the required structure with Status, Context, Decision, Alternatives Considered, Rationale, and Consequences sections. Each ADR addresses decisions that affect integration between frontend and backend, had viable alternatives with significant tradeoffs, and will impact Phase III (AI chatbot integration). The ADRs were saved in the correct location: history/adr/

## Outcome

The architectural decisions for Phase II have been properly documented with 7 comprehensive ADRs that explain the rationale behind key technical choices, consider alternatives, and evaluate the impact on future phases of the project. All ADRs follow the required format and are stored in the correct location.