# ADR-009: User ID in URL Path for API Endpoints

## Status
Accepted

## Context
The API needs to ensure proper user isolation by filtering all requests by authenticated user. We needed to decide how to pass the user ID in API requests - whether in the URL path, query parameters, or rely solely on the JWT token for identification.

## Decision
We will include user_id as a path parameter in API endpoints (e.g., `/api/{user_id}/tasks`).

## Alternatives Considered
1. **User ID from JWT Token Only**:
   - Pro: Simpler URL structure
   - Pro: No risk of user accessing wrong data through URL manipulation
   - Pro: More secure by design
   - Con: Less explicit about which user data is being accessed
   - Con: Harder to debug and trace requests
   - Impact on Phase III: More secure but potentially harder for AI chatbot to work with

2. **User ID in Query Parameters**:
   - Pro: Flexible URL structure
   - Pro: Easy to modify for different filtering options
   - Con: URLs become longer and less RESTful
   - Con: Query parameters might be logged in server logs
   - Impact on Phase III: Less RESTful structure for AI chatbot API interactions

3. **User ID in Path (Chosen)**:
   - Pro: RESTful API design
   - Pro: Clear, explicit about which user's data is being accessed
   - Pro: Good for API documentation and understanding
   - Pro: Follows common REST patterns
   - Con: Requires validation to ensure JWT user matches path user
   - Impact on Phase III: Clear API structure that will be easier for AI chatbot to understand

## Rationale
The user_id in path approach was chosen because it follows RESTful API design principles and makes it clear which user's data is being accessed. While it requires additional validation to ensure the JWT user matches the path user, this validation is straightforward to implement and provides an extra layer of security. The explicit path parameter makes the API more understandable and easier to document.

## Consequences
- Positive: RESTful API design that's easy to understand
- Positive: Clear identification of which user's data is being accessed
- Positive: Good for API documentation
- Negative: Requires additional validation to ensure JWT user matches path user
- Impact on Phase III: Clear, RESTful API structure that will be easier for AI chatbot to interact with