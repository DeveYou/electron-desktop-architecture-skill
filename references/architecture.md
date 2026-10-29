# Reference architecture: modular monolith, ports and adapters

## Process diagram

```text
                           UNTRUSTED UI BOUNDARY
┌───────────────────────────────────────────────────────────────┐
│ RENDERER (React, no Node/Electron APIs)                       │
│ App shell / routes / module presentations                      │
│    feature UI → application use cases → domain models         │
│                        ↓ ports                                │
│                 renderer adapters                             │
└──────────────────────┬────────────────────────────────────────┘
                       │ window.desktop.<explicitCapability>()
                       ▼ typed/limited preload bridge
===================== IPC TRUST BOUNDARY ========================
                       │ sender + schema + authority checked
┌──────────────────────▼────────────────────────────────────────┐
│ MAIN (privileged)                                              │
│ validated IPC adapter → application service → domain          │
│                                  ↓ ports                      │
│                       DB / FS / OS / network adapters         │
│ app composition root, lifecycle, native windows, tray, menus  │
└───────────────────────────────────────────────────────────────┘
     ▲                               ▲
     │                               │
 shared/contracts (types, schemas, channel IDs, serializable DTOs)
```

## Default project structure

```text
project/
├── docs/
│   ├── architecture.md               # project-specific decisions
│   └── adr/                          # decisions that change architecture
├── resources/                        # signed/packaged icons and assets
├── src/
│   ├── main/
│   │   ├── index.ts                   # app lifecycle, thin composition root
│   │   ├── app/
│   │   │   ├── create-window.ts
│   │   │   ├── register-ipc.ts
│   │   │   ├── security.ts
│   │   │   └── services.ts
│   │   └── modules/
│   │       └── settings/
│   │           ├── domain/
│   │           ├── application/
│   │           ├── infrastructure/
│   │           ├── ipc/
│   │           └── index.ts
│   ├── preload/
│   │   └── index.ts                   # narrow typed surface ONLY
│   ├── renderer/
│   │   ├── index.html
│   │   └── src/
│   │       ├── main.tsx
│   │       ├── app/
│   │       │   ├── App.tsx
│   │       │   ├── providers/
│   │       │   ├── navigation/
│   │       │   └── styles/
│   │       ├── modules/
│   │       │   └── settings/
│   │       │       ├── domain/
│   │       │       ├── application/
│   │       │       ├── infrastructure/
│   │       │       ├── presentation/
│   │       │       └── index.ts
│   │       └── shared/
│   │           ├── ui/                # shadcn primitives, app-owned
│   │           ├── design-system/     # tokens/layout/composites
│   │           ├── hooks/
│   │           └── lib/
│   └── shared/
│       ├── contracts/                # versioned IPC DTOs + Zod
│       └── constants/
├── tests/
│   ├── e2e/
│   └── integration/
├── electron.vite.config.ts
├── package.json
└── ...
```

This maps to electron-vite's conventional main/preload/renderer entrypoints. `src/shared` must be configured as a workspace-independent import path compatible with the main, preload and renderer build configurations.

## Dependency rule

```text
UI / native adapters → application → domain
                    ↘ interfaces / ports ↗
```

- **Domain:** entities, value objects, invariants, pure validation/transformations. Zero dependencies on React, Electron, storage, network, or UI libraries.
- **Application:** use cases, commands, orchestration, application-level errors, ports/interfaces. Depends on domain; may receive injected services.
- **Infrastructure:** implement ports using IPC client, SQLite, HTTP, file system, OS APIs, and Electron. No domain rules here.
- **Presentation:** React components, hooks, view models, loading/error states. Calls application services or adapters through explicit feature entrypoints.
- **Composition roots:** app bootstrap instantiates implementations and wires interfaces; no hidden global singleton containers by default.

## Module ownership rules

1. Organize business features (`library`, `downloads`, `chat`, `settings`), not huge top-level `components`, `services`, `utils` bags.
2. Each feature exports a narrow `index.ts`. Cross-feature imports target only public entrypoints; do not import another feature's `internal` files.
3. App shell coordinates navigation and global layout but must not become the god module for business workflows.
4. Features cannot import Electron directly from renderer. They call typed ports.
5. Shared UI contains domain-agnostic primitives. Feature-specific components stay in that feature; avoid dumping them into shared.
6. Separate main and renderer module folders when a capability spans both. They share **contracts**, not internal implementation code.
7. Record ownership for data, events, mutations, and side effects. A feature must have one authoritative write owner.
8. Circular dependencies are defects. Enforce with ESLint import rules / dependency-cruiser / equivalent.

## Scaling guidance

- **Small:** `presentation/`, `application/`, `index.ts` may suffice; do not create empty layers.
- **Medium:** split into domain/application/infrastructure/presentation once behavior and adapters exist.
- **Large:** add workspace packages only for independently testable bounded contexts with legitimate independent ownership or reuse. Keep process boundaries explicit.
- **Performance:** profile before adding workers/utility processes. Avoid synchronous file IO, huge JSON clones, and frequent IPC round trips.

## Errors and consistency

- Use typed domain errors; translate at adapters into stable, non-sensitive DTOs.
- Propagate cancellation where meaningful; dispose subscriptions when views unmount/windows close.
- Migrations, transaction boundaries, and recovery semantics belong to authoritative persistence service.
- Favor idempotent commands for retry-sensitive operations and event payloads with version/sequence when eventual sync requires it.
