---
name: electron-desktop-architecture
description: Design, scaffold, extend, review, or modernize secure cross-platform Electron desktop applications using React, TypeScript, electron-vite, Tailwind CSS, shadcn/ui, and module-driven clean architecture. Use for desktop app foundations, feature modules, typed IPC, desktop design systems, state management, testing, packaging, and maintainability audits. Do not use for browser-only websites or non-Electron desktop runtimes unless comparing migration options.
license: MIT
metadata:
  version: "1.0.0"
  category: "desktop-engineering"
---

# Electron Desktop Architecture

An agent-neutral engineering playbook. Prefer correct, secure, accessible, maintainable code over an impressive-looking but fragile demo. Follow existing repository choices unless explicitly tasked with migration. Do not silently replatform, upgrade major dependencies, or overwrite unrelated code.

## Working protocol

1. **Inspect before editing.** Read package scripts, build configuration, existing module boundaries, design tokens, tests, release setup, and applicable repository instructions. Determine whether the task is `bootstrap`, `feature`, `UI`, `native capability`, `refactor`, `audit`, or `release`.
2. **Clarify only consequential uncertainty.** If the product/platform is unspecified, default to Windows, macOS, and Linux; TypeScript strict mode; React + Vite via electron-vite; Electron; Tailwind CSS; shadcn/ui; Lucide; Zustand when needed; TanStack Query for remote data; Vitest + React Testing Library; optional Playwright Electron E2E. Use current compatible stable dependencies verified at implementation time; never invent version compatibility.
3. **Map module boundaries before code.** Define the feature's owner, public API, domain behavior, use cases, ports, adapters, processes, permissions, persistence, events, and acceptance tests. For trivial features, use fewer files. Read [architecture](references/architecture.md) and [module contracts](references/modules.md).
4. **Enforce Electron trust boundaries.** The renderer is untrusted for privileged operations. Keep Node/Electron APIs in main/preload only. Expose narrow, typed capabilities through preload and validate sender, payload, and authorization again in main. Read [security](references/security.md) and [IPC](references/ipc.md) before any native work.
5. **Build UI from the design system.** Reuse semantic tokens and accessible primitives; design for keyboard, focus, reduced motion, density, resizing, platform chrome, and light/dark variants. Read [design system](references/design-system.md) before styling.
6. **Choose data ownership intentionally.** Local presentation state stays in React; shared ephemeral state may use Zustand; remote server state uses TanStack Query; persistent/native state is owned by a main-process service or backend. Read [state and persistence](references/state-and-data.md).
7. **Implement in vertical slices.** Schema/contract → domain/use case → main adapter/IPC → preload facade → renderer adapter/hook → feature UI → tests. Do not create unused abstractions or generic base classes.
8. **Verify before declaring done.** Run available format, lint, typecheck, unit/component, boundary, security, build, and applicable E2E checks. Record what ran, what did not run, and remaining risks. See [testing](references/testing.md), [delivery](references/delivery.md), and [review checklist](references/review-checklist.md).

## Non-negotiable boundaries

- Main owns native privileges, file system, OS integration, secure storage, windows, menus, and privileged IPC handlers.
- Preload is a **minimal capability bridge**, not a second application or a generic event bus.
- Renderer owns React composition, navigation, forms, views, UI state, and presentation adapters. It never imports `electron`, Node built-ins, or main-process modules.
- `shared/contracts` contains serializable DTOs, IPC channel names, and runtime schemas; it does not import Electron, React, runtime secrets, or persistence drivers.
- Domain and use cases have **inward dependencies**. UI and infrastructure depend on domain/application, not vice versa. Modules communicate through exported public APIs or an explicit orchestration layer, not deep imports or arbitrary global stores.
- Favor **modular monolith** as the default. Separate packages/processes only for measured isolation, ownership, or distribution needs.
- Build secure by default: `contextIsolation: true`, `sandbox: true`, `nodeIntegration: false`, restrictive CSP, denied by default permissions/navigation, safe external URLs, sender checks, runtime schema validation. Never expose raw `ipcRenderer` to web content.
- Avoid premature microservices, monorepos, plugin systems, heavy state libraries, custom component libraries, or CQRS/event sourcing without a concrete need.

## Task-specific reference routing

| Task | Read first |
| --- | --- |
| New app / technology selection | [Stack](references/stack.md), [Architecture](references/architecture.md), [Bootstrap](references/workflows.md) |
| New feature/module | [Modules](references/modules.md), [IPC](references/ipc.md), [Example](examples/settings-feature/README.md) |
| UI/theme/UX work | [Design system](references/design-system.md), [State](references/state-and-data.md) |
| File system/native feature | [Security](references/security.md), [IPC](references/ipc.md) |
| Testing / technical debt | [Testing](references/testing.md), [Review](references/review-checklist.md) |
| CI / distribution / updating | [Delivery](references/delivery.md) |
| Architectural choice | [ADRs](references/decisions.md) |

## Expected agent outputs

- **Bootstrap:** selected stack with rationale; repository tree; process-boundary diagram; scripts; security setup; one vertical feature; design tokens; baseline tests; release risks.
- **Feature:** short boundary plan; explicitly owned files; implementation; validation; tests; migrations if needed; public API updates.
- **Audit:** findings ranked by severity with file/line evidence and remediation; no false claims about tests or compatibility.
- **Review:** change summary, tradeoffs, verified commands/results, skipped checks, remaining risks.

## Using bundled helpers

- `python3 scripts/validate_skill.py .` validates this bundle without installing dependencies.
- `python3 scripts/install_skill.py --help` prints supported agent targets and explicit installation options; use `--dry-run` first.
- `python3 scripts/new_module.py --help` previews a feature module scaffold and can create one without replacing existing files.
- `assets/agent-rules/` includes optional thin repository guidance files for agents that also read AGENTS.md, CLAUDE.md, or GEMINI.md.

Treat code snippets as patterns to adapt, not as security guarantees. Check latest authoritative documentation before generating dependencies, build options, or release pipelines. Source links: [sources](references/sources.md).
- `python3 scripts/check_boundaries.py /path/to/project` performs an advisory static check for common process/security boundary mistakes; it cannot prove security.
