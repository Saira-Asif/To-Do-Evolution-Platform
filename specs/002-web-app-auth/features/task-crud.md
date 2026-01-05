# Task CRUD Feature Specification

## Feature Overview
The Task CRUD (Create, Read, Update, Delete) feature provides the core functionality for users to manage their tasks in the Todo Web Application. This feature enables users to create, view, update, and delete tasks with proper validation and user isolation.

## User Stories

### US1: Task Creation
**As a** registered user
**I want** to create new tasks with title and description
**So that** I can track my pending work and responsibilities

**Acceptance Criteria:**
- Given I am logged in to the application
- When I navigate to the task creation form
- And I provide a title (1-200 characters) and optional description (max 1000 characters)
- Then the task should be created successfully and appear in my task list

**Success Scenario:**
1. User fills in the task title (required, 1-200 characters)
2. User optionally adds a description (max 1000 characters)
3. User submits the form
4. System validates input and creates the task
5. Task appears in the user's task list with "completed" set to false by default

**Error Scenarios:**
- If title is missing or exceeds 200 characters, show validation error
- If description exceeds 1000 characters, show validation error
- If user is not authenticated, redirect to login page

### US2: Task Reading (List)
**As a** registered user
**I want** to view all my tasks in a list
**So that** I can see what work I need to do

**Acceptance Criteria:**
- Given I am logged in to the application
- When I navigate to the tasks page
- Then I should see all tasks associated with my account
- And each task should display its title, description, and completion status

**Success Scenario:**
1. User navigates to tasks page
2. System retrieves all tasks for the authenticated user
3. Tasks are displayed in a list with relevant information
4. User can see completion status for each task

**Error Scenarios:**
- If user is not authenticated, redirect to login page
- If no tasks exist, show appropriate empty state

### US3: Task Reading (Details)
**As a** registered user
**I want** to view details of a specific task
**So that** I can see all information about that particular task

**Acceptance Criteria:**
- Given I am logged in to the application
- When I click on a specific task
- Then I should see detailed information about that task
- And I should only see tasks that belong to me

**Success Scenario:**
1. User clicks on a task from the list
2. System retrieves the specific task details
3. Task details are displayed with all relevant information
4. User can see creation and update timestamps

**Error Scenarios:**
- If user is not authenticated, redirect to login page
- If task doesn't exist or doesn't belong to user, show 404 error

### US4: Task Update
**As a** registered user
**I want** to update my task details
**So that** I can modify the title, description, or completion status

**Acceptance Criteria:**
- Given I am logged in to the application
- When I edit a task and submit the changes
- Then the task should be updated with the new information
- And I should only be able to update tasks that belong to me

**Success Scenario:**
1. User selects a task to edit
2. User modifies the title, description, or completion status
3. User saves the changes
4. System validates input and updates the task
5. Updated task is reflected in the task list

**Error Scenarios:**
- If title exceeds 200 characters, show validation error
- If description exceeds 1000 characters, show validation error
- If user is not authenticated, redirect to login page
- If task doesn't belong to user, show 403 forbidden error

### US5: Task Completion Toggle
**As a** registered user
**I want** to mark tasks as complete or incomplete
**So that** I can track my progress and completed work

**Acceptance Criteria:**
- Given I am logged in to the application
- When I toggle the completion status of a task
- Then the task's completion status should update
- And the change should be persisted in the database

**Success Scenario:**
1. User finds a task in their list
2. User toggles the completion status (e.g., clicking a checkbox)
3. System updates the task's completion status
4. Updated status is reflected in the UI

**Error Scenarios:**
- If user is not authenticated, redirect to login page
- If task doesn't belong to user, show 403 forbidden error

### US6: Task Deletion
**As a** registered user
**I want** to delete tasks I no longer need
**So that** I can keep my task list clean and organized

**Acceptance Criteria:**
- Given I am logged in to the application
- When I delete a task after confirmation
- Then the task should be removed from my task list
- And I should only be able to delete tasks that belong to me

**Success Scenario:**
1. User selects a task to delete
2. User confirms the deletion (to prevent accidental deletions)
3. System removes the task from the database
4. Task is removed from the user's task list

**Error Scenarios:**
- If user is not authenticated, redirect to login page
- If task doesn't belong to user, show 403 forbidden error
- If task doesn't exist, show 404 error

## Technical Requirements

### API Endpoints
- `GET /api/{user_id}/tasks` - List all user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task details
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status

### Data Validation
- **Title**: Required, 1-200 characters, no control characters
- **Description**: Optional, max 1000 characters, no control characters
- **Completed**: Boolean value, default false for new tasks
- **User ID**: Must match authenticated user

### Security Requirements
- All endpoints require valid JWT authentication
- User ID in URL path must match JWT token user ID
- Users can only access their own tasks
- Return 403 Forbidden for unauthorized access attempts

### Performance Requirements
- API operations complete within 2 seconds
- Support for 100+ tasks per user without performance degradation
- Efficient database queries with proper indexing

### Error Handling
- Proper HTTP status codes (200, 201, 400, 401, 403, 404, 422, 500)
- Consistent error response format
- Validation error messages for client-side feedback

## User Interface Requirements

### Task Creation Form
- Input field for task title (required)
- Textarea for task description (optional)
- Clear validation messages
- Loading state during submission
- Success feedback after creation

### Task List View
- Display all tasks with title and completion status
- Visual indication of completed vs incomplete tasks
- Ability to sort/filter tasks
- Pagination for large task lists
- Empty state when no tasks exist

### Task Detail View
- Display all task information (title, description, status, timestamps)
- Edit and delete controls
- Clear navigation back to task list

### Task Editing
- Pre-populated form with existing values
- Same validation as creation
- Clear indication of saving state
- Feedback on successful updates

## Business Rules
- Tasks are owned by the user who created them
- Users cannot modify or view other users' tasks
- New tasks are created with completed = false by default
- Task titles must be unique within a user's task list (optional rule)
- Tasks cannot be permanently deleted, only soft-deleted (optional rule)

## Constraints
- All API calls must be authenticated
- Data must be persisted in PostgreSQL database
- Frontend must be responsive and work on mobile devices
- All user inputs must be validated on both frontend and backend
- No manual coding - all implementation via Claude Code

## Dependencies
- Authentication system for user identification
- Database for task persistence
- Frontend framework for UI components
- API framework for backend endpoints

## Success Metrics
- 100% of CRUD operations complete successfully for authenticated users
- Tasks persist correctly in PostgreSQL database
- Users can only access their own tasks (user isolation maintained)
- Responsive UI works on mobile and desktop devices
- API operations complete within 2 seconds