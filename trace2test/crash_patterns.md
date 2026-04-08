# Trace2Test Crash Pattern Database

This file contains a curated set of high-level real-world crash patterns that Bob can use for root cause analysis, test generation, and fix guidance during the Trace2Fix workflow.

## Pattern 1 — Division by Zero
- Error signals:
  - `ZeroDivisionError`
  - `ArithmeticException: / by zero`
- Common cause:
  - A divisor derived from user input, configuration, or upstream data is `0`
- Typical reproduction strategy:
  - Re-run the failing function with the exact numeric inputs from the crash log
- Safe fix guidance:
  - Validate the divisor before division and raise a domain-specific validation error

## Pattern 2 — Null / None Dereference
- Error signals:
  - `AttributeError: 'NoneType' object has no attribute ...`
  - `NullPointerException`
- Common cause:
  - An object expected to be initialized is missing due to invalid input, failed lookup, or unhandled optional data
- Typical reproduction strategy:
  - Pass missing or null-like inputs matching the production call path
- Safe fix guidance:
  - Add null checks, guard clauses, or defaults before dereferencing values

## Pattern 3 — Index Out of Bounds
- Error signals:
  - `IndexError: list index out of range`
  - `ArrayIndexOutOfBoundsException`
- Common cause:
  - Code accesses a list or array position that does not exist
- Typical reproduction strategy:
  - Reproduce with an empty or shorter-than-expected collection
- Safe fix guidance:
  - Validate collection length or iterate safely instead of direct indexing

## Pattern 4 — Key / Property Missing
- Error signals:
  - `KeyError`
  - `NoSuchElementException`
  - missing object property access patterns
- Common cause:
  - Assumed dictionary, map, or object fields are absent in real-world payloads
- Typical reproduction strategy:
  - Replay the failing request with the missing key or property omitted
- Safe fix guidance:
  - Use safe access methods, defaults, schema validation, or explicit input checks

## Pattern 5 — Invalid Type Conversion
- Error signals:
  - `ValueError`
  - `TypeError`
  - `NumberFormatException`
- Common cause:
  - Untrusted input cannot be parsed into the expected numeric, date, enum, or structured type
- Typical reproduction strategy:
  - Supply malformed or unexpected string input from logs
- Safe fix guidance:
  - Validate and sanitize inputs before conversion; return controlled errors

## Pattern 6 — File Not Found / Missing Resource
- Error signals:
  - `FileNotFoundError`
  - `ENOENT`
- Common cause:
  - Code expects a file, config, template, or generated artifact that is absent at runtime
- Typical reproduction strategy:
  - Run the same code path without the required file or resource present
- Safe fix guidance:
  - Check file existence, improve path handling, and fail with a clear message

## Pattern 7 — Permission Denied
- Error signals:
  - `PermissionError`
  - `EACCES`
  - access denied messages
- Common cause:
  - Runtime lacks permission to read, write, execute, or bind required resources
- Typical reproduction strategy:
  - Execute the failing operation in a restricted environment or on protected paths
- Safe fix guidance:
  - Validate permissions early, use allowed paths, and surface actionable remediation

## Pattern 8 — Timeout / External Dependency Stall
- Error signals:
  - timeout exceptions
  - request deadline exceeded
  - socket timeout
- Common cause:
  - Downstream APIs, databases, queues, or network calls exceed expected response time
- Typical reproduction strategy:
  - Mock or simulate a delayed dependency response
- Safe fix guidance:
  - Add timeouts, retries with limits, circuit breakers, and graceful fallbacks

## Pattern 9 — Connection Refused / Service Unavailable
- Error signals:
  - connection refused
  - `ECONNREFUSED`
  - service unavailable responses
- Common cause:
  - A dependent service is down, not listening, or misconfigured
- Typical reproduction strategy:
  - Run the code path while the target host or service is unavailable
- Safe fix guidance:
  - Detect dependency availability, add retry logic where appropriate, and fail gracefully

## Pattern 10 — Database Constraint Violation
- Error signals:
  - unique constraint violation
  - foreign key violation
  - integrity constraint errors
- Common cause:
  - Application writes invalid or duplicate data that violates database rules
- Typical reproduction strategy:
  - Repeat the write using the same conflicting payload or inconsistent parent-child data
- Safe fix guidance:
  - Validate invariants before insert/update and handle duplicate or invalid state safely

## Pattern 11 — Race Condition / Concurrent Mutation
- Error signals:
  - intermittent failures
  - duplicate processing
  - inconsistent state under load
- Common cause:
  - Shared state is modified concurrently without proper coordination
- Typical reproduction strategy:
  - Run repeated concurrent calls against the same state or resource
- Safe fix guidance:
  - Use locks, transactions, idempotency keys, or atomic operations

## Pattern 12 — Memory Exhaustion / Resource Leak
- Error signals:
  - out-of-memory messages
  - process killed
  - too many open files
- Common cause:
  - Objects, buffers, connections, or file handles accumulate without release
- Typical reproduction strategy:
  - Run the workload repeatedly or at scale until resource usage grows uncontrollably
- Safe fix guidance:
  - Close resources deterministically, stream large data, and monitor usage boundaries

## Pattern 13 — Infinite Recursion / Stack Overflow
- Error signals:
  - `RecursionError`
  - stack overflow
- Common cause:
  - Recursive logic misses a termination condition or cycles through data unexpectedly
- Typical reproduction strategy:
  - Supply inputs that trigger the recursive cycle from the failing path
- Safe fix guidance:
  - Add base cases, cycle detection, or convert to iterative logic

## Pattern 14 — Assertion / State Invariant Failure
- Error signals:
  - assertion failed
  - illegal state
  - invariant violation
- Common cause:
  - Internal assumptions about program state no longer hold under real input or timing
- Typical reproduction strategy:
  - Replay the sequence of calls that led to the invalid state
- Safe fix guidance:
  - Validate state transitions explicitly and handle invalid states predictably

## Pattern 15 — Serialization / Deserialization Failure
- Error signals:
  - JSON parse errors
  - schema mismatch
  - unmarshalling or decoding exceptions
- Common cause:
  - Input payload shape differs from expected schema or contains malformed data
- Typical reproduction strategy:
  - Reuse the raw payload from logs or a reduced version containing the malformed field
- Safe fix guidance:
  - Add schema validation, backward-compatible parsing, and better error reporting

## Pattern 16 — Deadlock / Thread Hang
- Error signals:
  - request hangs indefinitely
  - blocked thread dumps
  - no progress with active process still running
- Common cause:
  - Two or more threads, locks, or transactions wait on each other in a circular dependency
- Typical reproduction strategy:
  - Replay concurrent operations in the same order and timing window seen in production
- Safe fix guidance:
  - Enforce consistent lock ordering, reduce lock scope, or replace blocking coordination with safer primitives

## Pattern 17 — Transaction Boundary / Partial Commit Failure
- Error signals:
  - data partially updated after failure
  - inconsistent records across related tables or services
  - rollback not applied as expected
- Common cause:
  - Multi-step write logic is not wrapped in a proper transaction or spans unreliable boundaries
- Typical reproduction strategy:
  - Re-run the exact write sequence and force a failure in the middle step
- Safe fix guidance:
  - Use atomic transactions, compensating actions, or explicit rollback-safe workflow design

## Pattern 18 — Cache Invalidation / Stale Data Crash
- Error signals:
  - old data returned after update
  - intermittent state mismatch
  - deserialization or lookup failures after deployment
- Common cause:
  - Cached entries no longer match source-of-truth data, schema, or permissions
- Typical reproduction strategy:
  - Replay reads after updates while preserving stale cache state
- Safe fix guidance:
  - Add cache versioning, explicit invalidation, and fallback-to-source behavior on mismatch

## Pattern 19 — Schema Drift / Migration Mismatch
- Error signals:
  - missing column
  - unknown field
  - incompatible schema version errors
- Common cause:
  - Application code and runtime database/event/message schema versions are out of sync
- Typical reproduction strategy:
  - Run the current code against the prior schema or replay payloads from before migration
- Safe fix guidance:
  - Make migrations backward compatible, gate rollout order, and add schema-version checks

## Pattern 20 — Date/Time Boundary Failure
- Error signals:
  - invalid date comparisons
  - timezone conversion exceptions
  - bugs only at midnight, month-end, DST, or leap-day boundaries
- Common cause:
  - Business logic assumes local time, fixed offsets, or simple calendar arithmetic
- Typical reproduction strategy:
  - Re-run with timestamps at the exact boundary conditions from logs
- Safe fix guidance:
  - Normalize to UTC internally, use timezone-aware libraries, and test critical calendar boundaries

## Pattern 21 — Floating-Point Precision / Rounding Defect
- Error signals:
  - equality checks fail unexpectedly
  - totals differ by small amounts
  - threshold logic flips near numeric boundaries
- Common cause:
  - Decimal-sensitive business logic is implemented with floating-point math
- Typical reproduction strategy:
  - Replay the exact numeric inputs that sit near rounding or equality thresholds
- Safe fix guidance:
  - Use decimal/fixed-point types, explicit rounding rules, and tolerance-aware comparisons where appropriate

## Pattern 22 — Duplicate Event / Retry Replay Failure
- Error signals:
  - double charges
  - duplicate emails
  - repeated state transitions after retry
- Common cause:
  - Handlers are retried or messages are delivered more than once without idempotency protection
- Typical reproduction strategy:
  - Re-send the same event or request multiple times with identical identifiers
- Safe fix guidance:
  - Add idempotency keys, de-duplication storage, and replay-safe handlers

## Pattern 23 — Async Ordering / Eventual Consistency Bug
- Error signals:
  - entity not found immediately after creation
  - dependent job runs before source state is visible
  - flaky failures under distributed timing
- Common cause:
  - Asynchronous workers or replicated systems observe state in a different order than expected
- Typical reproduction strategy:
  - Reproduce the same event sequence with delayed propagation or reordered async tasks
- Safe fix guidance:
  - Add readiness checks, retries with bounded backoff, and event ordering guarantees where required

## Pattern 24 — Thread-Unsafe Shared Client / Singleton Misuse
- Error signals:
  - random corruption
  - non-deterministic crashes under load
  - state leaking between requests
- Common cause:
  - A shared mutable client, singleton, or global object is reused across concurrent requests unsafely
- Typical reproduction strategy:
  - Run concurrent requests through the same shared instance while preserving production-like load
- Safe fix guidance:
  - Remove shared mutable state, use per-request instances, or protect access with proper synchronization

## Pattern 25 — Cleanup / Finalizer Order Failure
- Error signals:
  - use-after-close
  - resource already disposed
  - shutdown-only crashes
- Common cause:
  - Teardown logic closes resources in the wrong order or background work continues after cleanup starts
- Typical reproduction strategy:
  - Replay shutdown, cancellation, or error-cleanup paths with the same operation ordering
- Safe fix guidance:
  - Make cleanup idempotent, stop producers before consumers, and guard resource usage after teardown

## How to Use This Database
- Match the error type and traceback in [trace2test/crash.log](trace2test/crash.log) against the closest pattern
- Extract the exact failing inputs from the log
- Generate a regression test that reproduces the observed failure
- Apply the smallest safe fix that converts uncontrolled crashes into validated behavior
- Re-run the generated test to verify the fix