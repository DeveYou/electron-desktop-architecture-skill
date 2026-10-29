# State ownership, persistence, and synchronization

## State location decision tree

1. Needed by one component or one form? → `useState`, `useReducer`, or form library.
2. Needed by a few siblings? → lift to a feature-level provider/composition root.
3. Shared, transient renderer state across features? → a focused Zustand store with selectors; do not convert it into a persistence layer.
4. Remote server cache? → TanStack Query with stable query keys, invalidations, retry/backoff, offline policy and suspense policy chosen explicitly.
5. Native OS state or local persisted records? → main-owned service; renderer accesses a typed IPC adapter.
6. Sensitive credentials? → appropriate OS-secure facility, never plain renderer storage.

## Command and query separation (pragmatic)

- Reads can use a typed query port; mutations use explicit commands whose side effects are centralized.
- Renderer cache is not a source of truth for persistence. Refresh after mutations or consume validated change events.
- Choose optimistic updates only when rollback and conflict UX are defined.
- Persist settings atomically, validate on read, apply migrations on version changes, provide defaults when corrupt, and preserve user data safely.
- SQLite for structured data: schema migrations, transactions for multi-record consistency, prepared statements, bounded queries, WAL only when suitable and tested, and explicit backup/recovery behavior.

## Lifecycle and errors

- Model `idle/loading/success/empty/error` as actual states rather than a pile of booleans.
- Cancel obsolete async requests (AbortSignal if supported), handle unmount and window closure.
- Disallow unbounded subscription fan-out, event listener leaks, or stale closures.
- Surface recoverable errors with a retry path; log detailed diagnostics in trusted process with redaction and opt-in telemetry considerations.
- Define sync policy when user has multiple devices: server source of truth vs local-first, conflict handling, offline edits, and migration strategy.

## Performance

- Keep React rerenders scoped with selectors and component ownership; do not memoize everything by reflex.
- Throttle/debounce hot-path IPC, search, and filesystem watching when necessary.
- Avoid synchronous large disk scans in main, heavy CPU on UI thread, excessive data copying, and giant JSON payloads.
- Measure startup time, memory, interactions, and energy impact on representative hardware before tuning budgets.
