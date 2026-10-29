# Architecture / release review checklist

## Architecture

- [ ] Every business capability has a clear owning module.
- [ ] Domain/application layers are isolated from React/Electron/storage.
- [ ] Feature public entrypoints are stable and cross-module dependencies are explicit.
- [ ] No circular imports, barrel loops, or god `shared` utilities.
- [ ] Cross-process DTOs are serializable and runtime validated.
- [ ] Simple features are not overengineered.

## Electron security

- [ ] context isolation, sandbox, no Node integration in renderer, webSecurity enforced.
- [ ] No raw/generic renderer-to-main IPC bridge; per-operation methods only.
- [ ] Main checks sender window/frame/origin, payload schema, and authority.
- [ ] Permissions and window creation/navigation deny by default.
- [ ] External URLs, file paths, and imported content are validated and constrained.
- [ ] CSP, custom app protocol, Electron fuses, secrets, logs reviewed.

## UI & data

- [ ] Semantic design tokens; light/dark modes; keyboard and screen reader path.
- [ ] Visible focus, reduced-motion support and error/empty/loading states.
- [ ] Window min sizes, resizing, zoom, OS titlebar behavior tested.
- [ ] Exactly one authoritative write owner for persisted data.
- [ ] IPC subscriptions and async work disposed or canceled correctly.

## Quality & release

- [ ] Format, lint, typecheck, unit/component/build gates pass.
- [ ] IPC hostile-input/security boundary tests pass.
- [ ] Representative E2E smoke and target OS checks pass or gaps documented.
- [ ] Installer/signature/updater/migrations tested if being released.
- [ ] User-data recovery and crash/error path documented.
- [ ] Agent report includes what was not verified.
