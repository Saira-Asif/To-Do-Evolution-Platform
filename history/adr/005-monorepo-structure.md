# ADR-005: Monorepo Structure for Full-Stack Application

## Status
Accepted

## Context
The Phase II Full-Stack Web Application requires both a frontend (Next.js) and backend (FastAPI) component that need to work together. We needed to decide how to structure these components in terms of repository organization. The decision impacts development workflow, dependency management, deployment strategies, and future phases of development.

## Decision
We will use a monorepo structure with both frontend and backend in a single repository.

## Alternatives Considered
1. **Separate Repositories (Multi-repo)**:
   - Pro: Independent development and deployment cycles
   - Pro: Clear separation of concerns
   - Pro: Independent scaling of teams
   - Con: Complex dependency management between services
   - Con: Cross-cutting changes require multiple PRs
   - Con: More complex CI/CD setup
   - Impact on Phase III: More complex integration of AI chatbot with frontend/backend

2. **Git Submodules**:
   - Pro: Maintains separate repo benefits while allowing composition
   - Pro: Clear version pinning of dependencies
   - Con: Complex development workflow
   - Con: Difficult for developers to make cross-cutting changes
   - Con: Potential for submodule reference issues
   - Impact on Phase III: Complex to integrate AI chatbot as separate service

3. **Monorepo (Chosen)**:
   - Pro: Single context for AI tools like Claude Code
   - Pro: Easier cross-cutting changes (e.g., add field to Task model)
   - Pro: Shared types between frontend and backend
   - Pro: Simpler development workflow
   - Pro: Atomic commits for cross-service changes
   - Con: Larger repository size
   - Con: Potential for tight coupling between services
   - Impact on Phase III: Easier integration of AI chatbot as it can reference both frontend and backend code

## Rationale
The monorepo approach was chosen primarily because it works well with Claude Code's AI-first development approach, allowing the AI to see the entire project in a single context. This is particularly important for making cross-cutting changes that affect both frontend and backend. The shared types between frontend and backend will also be beneficial for type-safe API client generation. Additionally, the simpler development workflow aligns with the hackathon's focus on rapid development.

## Consequences
- Positive: Easier for Claude Code to work with entire project context
- Positive: Simplified dependency management between frontend and backend
- Positive: Atomic commits for changes affecting both services
- Positive: Shared types and interfaces between frontend and backend
- Negative: Larger repository size and potential for tight coupling
- Impact on Phase III: The monorepo structure will facilitate easier integration of the AI chatbot as it can reference both frontend and backend components