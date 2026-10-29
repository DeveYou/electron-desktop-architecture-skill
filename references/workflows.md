# Agent implementation playbooks

## A. Bootstrap a new product

1. Read requirements; distinguish platforms, online/offline operation, native capabilities, threat sensitivity, data durability, distribution and design character.
2. Create a one-page decision sheet: Electron/electron-vite baseline, module boundaries, persistence choice, expected IPC, installer choice, minimum platform versions, security model, test matrix.
3. Create an official electron-vite React TypeScript starter using its current documentation. **Do not invent unverified CLI flags or versions.**
4. Enable strict TypeScript, lint/format, path boundaries and scripts that work locally + CI.
5. Create `src/shared/contracts`, `src/main/app`, `src/main/modules`, `src/preload`, `src/renderer/src/app`, `src/renderer/src/modules`, `src/renderer/src/shared`.
6. Establish secure BrowserWindow, session, navigation, external link, permission and CSP policies, with platform-specific caveats.
7. Implement one end-to-end thin settings feature, including runtime validation and safe IPC; ensure renderer has no Node/Electron imports.
8. Install Tailwind/shadcn according to current documentation, set semantic tokens, AppShell, nav, 2 theme states, accessible shell interactions.
9. Add tests and verify end-to-end workflow in dev/build; create README, `.env.example` (no secrets), architecture doc and first ADR.
10. Decide on packaging after requirements, implement release gates, avoid premature updater integration.

## B. Add a feature

1. Read feature ownership and current public APIs.
2. Create a `Module design card` per [modules](modules.md); adapt folders to complexity.
3. Add pure domain/use-case code and unit tests first.
4. If native, introduce contract schemas + main handler + preload method; include malicious inputs/forged IPC tests.
5. Add renderer infrastructure adapter and hook; keep feature logic out of generic `shared/`.
6. Build UI with existing tokens, accessible primitives and state feedback; add unit/component and smoke tests.
7. Update module barrel and application composition root; run quality gates; record deviations.

## C. Refactor an existing desktop app

1. Generate current dependency/process map; identify privilege leaks, circular dependencies, fragmented design tokens, duplicated state and high-churn modules.
2. Report a severity-ranked migration plan; prioritize security defects and reliable tests.
3. Add seams/ports around existing code before moving files; migrate one vertical feature at a time with stable public APIs.
4. Avoid a big-bang rewrite without a tested migration strategy and explicit authorization.
5. Measure before/after outcomes: coupling graph, test coverage, build/startup metrics and UX regressions.

## D. Audit/review

- Security: renderer/node imports, preload generic IPC, sender checks, schema validation, navigation, permissions, CSP, protocol, external URL handling.
- Architecture: feature ownership, public barrels, inward dependencies, cross-feature deep imports, accidental global mutable state, empty abstraction layers.
- UX: token consistency, focus, keyboard, scroll ownership, themes, responsive window behavior, reduced motion.
- Operability: logs/error handling, migrations, packaging, updates, tests and release verification.
- Output prioritized concrete findings with file paths and suggested minimal remediations.

## Delivery format for agents

```text
Decision summary (what/why)
Module/process diagram and affected public contracts
Files added/changed + purpose
Security and accessibility considerations
Commands run + actual results
Not run / environment limitations
Tradeoffs / follow-up tasks
```
