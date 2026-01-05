# ADR-001: In-Memory Storage Using Dict[UUID, Todo]

## Status
Accepted

## Context
Phase I of the Console Todo App requires a simple storage mechanism that maintains data during the application runtime. We need to choose an appropriate in-memory data structure that allows efficient lookup, insertion, and modification of todo items.

## Decision
We will use a Python dictionary with UUID keys mapping to Todo objects (`Dict[UUID, Todo]`) as the primary in-memory storage mechanism.

## Alternatives Considered
1. **List of Todo objects**:
   - Pro: Simple to implement and understand
   - Pro: Natural ordering based on insertion sequence
   - Con: O(n) lookup time for finding specific todos
   - Con: Less efficient for operations requiring specific todo retrieval

2. **Dictionary with integer keys (auto-increment)**:
   - Pro: Fast O(1) lookup time
   - Pro: Simple integer-based indexing
   - Con: Potential key conflicts if items are deleted
   - Con: Less robust for concurrent access patterns

3. **Dictionary with UUID keys (selected)**:
   - Pro: Fast O(1) lookup time
   - Pro: Globally unique identifiers prevent key conflicts
   - Pro: Safe for concurrent access patterns
   - Pro: Facilitates easier migration to persistent storage in Phase II
   - Con: Slightly more complex to generate UUIDs

## Rationale
The dictionary with UUID keys provides the best balance of performance and robustness. The O(1) lookup time is crucial for good performance as the number of todos grows. Using UUIDs eliminates potential issues with key conflicts that could occur with auto-incrementing integers, especially when items are deleted. This approach also makes future migration to persistent storage more straightforward since UUIDs are commonly used as primary keys in databases.

## Consequences
- Positive: Fast access to todos by ID, robust against key conflicts
- Positive: Natural migration path to persistent storage solutions
- Positive: Supports concurrent access patterns if needed in the future
- Negative: Slight overhead in UUID generation and storage
- Impact on Phase II: The UUID-based approach will facilitate direct migration to database storage with minimal code changes