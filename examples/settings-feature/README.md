# Settings feature: illustrative vertical slice

This example demonstrates how a minimal native-capability feature crosses the Electron trust boundary while staying modular. It is a **reference pattern**, not a standalone app, and intentionally omits full electron-vite config, app bootstrap, a complete persistent repository, and test harness. Copy/adapt files under `project-files/src/` into an existing electron-vite React/TypeScript application.

## Data path

```text
SettingsPanel (renderer)
  → useSettings (application/presentation adapter)
  → window.desktop.settings.* (infrastructure)
  → contextBridge preload facade
  → settings:get / settings:update-theme
  → main IPC (sender + schema + authorization checks)
  → SettingsService (use case)
  → SettingsRepository (main-owned persistence port)
```

## Integration instructions

1. Install `zod` and align TypeScript/JSX/module resolution with your starter. Use existing shadcn components in your actual UI; this example intentionally relies on native HTML controls to avoid template dependency on a specific UI kit version.
2. Copy contracts to `src/shared/contracts/settings.ts` and run the same validation on **both** main requests and returned data.
3. Wire `createSettingsService(repository)` from main composition root. Use a proper `SettingsRepository` adapter backed by atomic settings storage (or database) for real persistence; the included in-memory adapter is for tests and illustration only.
4. Call `registerSettingsIpc(window, service, guard)` **once per live IPC registration**. If app windows can be recreated, use lifecycle-aware authorized window state; dispose handlers on teardown and re-register correctly.
5. Merge the narrow preload `settings` property into your existing `window.desktop` bridge. Only call `contextBridge.exposeInMainWorld('desktop', ...)` **once**, in the final combined preload entrypoint.
6. Provide `Window.desktop` typing from a *type-only* import or a shared interface, and build `isTrustedSender` to match your exact dev/production app URL allowlist and allowed main frame.
7. Add tests for invalid theme, forged sender, persistence failures, UI loading/error states, and update race behavior.

## Design note

Settings are app-level data, but UI rendering remains a `settings` renderer feature. Persisted settings are main-owned; renderer gets read/command methods, not arbitrary filesystem permissions.
