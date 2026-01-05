# ADR-004: UUID for Task Identification

## Status
Accepted

## Context
The Console Todo App needs a reliable way to uniquely identify todo items. We must choose an identification strategy that ensures uniqueness, supports efficient lookups, and facilitates future migration to persistent storage.

## Decision
We will use UUID4 (randomly generated UUIDs) as the primary identifier for todo items.

## Alternatives Considered
1. **Auto-incrementing integers**:
   - Pro: Simple and intuitive for users
   - Pro: Compact representation
   - Pro: Natural ordering
   - Con: Potential conflicts when merging data from different sources
   - Con: Not suitable for distributed systems
   - Con: May reveal information about total task count

2. **UUID4 (randomly generated) (selected)**:
   - Pro: Globally unique with extremely high probability
   - Pro: No coordination needed for generation
   - Pro: Suitable for distributed systems
   - Pro: Secure (doesn't reveal information about task count or creation order)
   - Pro: Direct mapping to database UUID types in Phase II
   - Con: Longer, less human-friendly identifiers
   - Con: No natural ordering

3. **Hash-based identifiers**:
   - Pro: Deterministic generation
   - Pro: Could be based on content for idempotent creation
   - Con: Potential collisions with similar content
   - Con: Exposes content information in the ID
   - Con: More complex to implement securely

## Rationale
UUID4 was chosen because it provides strong guarantees of uniqueness without requiring coordination between different instances of the application. This is particularly important for future phases where we might implement synchronization or distributed features. The random nature of UUID4 ensures that the identifiers don't reveal information about the number of tasks or their creation order. The approach also maps directly to common database UUID types, making the migration to persistent storage in Phase II straightforward.

## Consequences
- Positive: Strong uniqueness guarantees without coordination
- Positive: Secure identifiers that don't leak information
- Positive: Direct compatibility with database UUID types in Phase II
- Positive: Supports distributed systems if needed later
- Negative: Less human-friendly identifiers for users
- Negative: No natural ordering of tasks by ID
- Impact on Phase II: UUID-based identification will seamlessly transition to database storage with no structural changes needed