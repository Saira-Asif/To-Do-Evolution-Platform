# Frontend - Claude Code Instructions

## Overview
This is the Next.js frontend for the Todo Web Application with authentication and responsive UI.

## Technology Stack
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth
- **HTTP Client**: ky
- **State Management**: React Query for server state, React Hook Form for form state
- **Form Handling**: React Hook Form with validation

## Project Structure
- `app/` - Next.js App Router pages and layouts
- `components/` - Reusable React components
- `lib/` - Utility functions and API clients
- `hooks/` - Custom React hooks
- `contexts/` - React context providers
- `public/` - Static assets

## Key Patterns
- Use Next.js App Router for file-based routing
- Implement responsive design with Tailwind CSS
- Use React Query for server state management and caching
- Implement form validation with React Hook Form
- Use context for global state like authentication
- Follow component composition patterns
- Use TypeScript for type safety

## Authentication Flow
- Better Auth handles user registration and login
- JWT tokens stored in localStorage
- Protected routes wrapper for authenticated pages
- Token validation and refresh handling

## API Integration
- ky HTTP client for API calls
- React Query hooks for data fetching and mutations
- Consistent error handling across API calls
- Loading and error state management

## Common Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linting
- `npm run type-check` - Run TypeScript type checking

## UI/UX Considerations
- Responsive design for mobile and desktop
- Loading states for API calls
- Error handling and user feedback
- Form validation and user input feedback
- Accessible components and proper semantic HTML