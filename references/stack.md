# Stack selection and defaults

## Baseline (verify stable compatible versions at implementation time)

- **Runtime:** Electron, with each app surface deliberately assigned to main, preload, or renderer.
- **Build:** electron-vite, React, TypeScript with `strict: true`, and strict linting. Use the official React+TS starter as a baseline; preserve build-specific path conventions.
- **Styles:** Tailwind CSS (current stable version), CSS custom properties, shadcn/ui components copied into the project, Radix primitives under the hood, Lucide icons. Treat shadcn components as project-owned code.
- **Animations:** CSS for basic transitions; Motion only when the interaction benefits and accessibility is respected.
- **Routing:** React Router if multiple independent pages or deep linking; a tiny typed view state is enough for simple apps.
- **Renderer state:** React state for local, Zustand for moderately shared transient state. Keep platform state outside generic UI stores.
- **Remote data:** TanStack Query when a remote API exists. Avoid it for purely synchronous local component state.
- **Validation:** Zod at IPC, network, configuration, file import boundaries; TypeScript alone is not runtime validation.
- **Local persistence:** main-process service. JSON/atomic settings for simple config; SQLite when structured queries, transactions or migrations justify it. Never persist sensitive tokens in plain JSON/SQLite by default.
- **Tests:** Vitest (domain/unit), React Testing Library (components), Playwright Electron E2E (smoke, supported platforms/CI constraints), static IPC/security checks.
- **Distribution:** choose Electron Forge or electron-builder based on installers/updates/publishing needs; avoid mixing packaging systems without reason.
- **Quality:** ESLint/Prettier (or a documented single equivalent), strict TS, accessibility checks, dependency update review, CI release gates.

## Optional / conditional

| Need | Add | Avoid unless needed |
| --- | --- | --- |
| Complex validated forms | React Hook Form + Zod integration | Large form abstraction for two inputs |
| Many complex views | React Router + route-level code-splitting | Custom routing framework |
| Rich local structured records | SQLite, repositories + migrations | SQLite for a handful of toggles |
| Real-time backend | Typed WebSocket events + reconnect/backpressure | Unbounded event subscribers |
| Heavy CPU/I/O | Worker thread / utility process | Blocking main process or using renderer as privileged worker |
| Advanced tables | TanStack Table / virtualizer | Rendering thousands of DOM rows |
| OS-level secrets | Keychain/Credential Locker via approved facility and threat model | Secrets in renderer/localStorage |
| Internationalization | ICU message tooling and locale-aware layout | Hard-coded strings scattered through components |

## Upgrade policy

1. Never guess exact library versions or platform support. Inspect lockfiles, release notes, and official migration guides.
2. Introduce a versioned dependency change separately from an unrelated feature when feasible.
3. Verify Electron, Node, TypeScript, Vite, Tailwind, shadcn and packaging compatibility together.
4. Explicitly test macOS/Windows/Linux paths and window integration. A cross-platform framework is not a substitute for OS tests.
5. Document the rationale for any departure from the baseline in an ADR.
