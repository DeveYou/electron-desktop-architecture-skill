# Typed, validated, least-privilege IPC

## Four-part contract

1. **Shared:** serializable DTO schemas and channel constants only.
2. **Main:** register named handlers; validate sender/origin, parse inputs, authorize operation/resource, invoke injected use case, map output to safe DTO.
3. **Preload:** expose specific promise-returning methods via `contextBridge`; never expose `ipcRenderer`, arbitrary channel dispatch, or Electron `event`.
4. **Renderer:** implements feature port using `window.desktop` methods. UI/domain cannot know about Electron internals.

## Example contract

```ts
// src/shared/contracts/settings.ts
import { z } from 'zod'
export const themeSchema = z.enum(['system', 'light', 'dark'])
export const updateThemeInputSchema = z.object({ theme: themeSchema }).strict()
export const settingsSchema = z.object({ theme: themeSchema }).strict()
export type Settings = z.infer<typeof settingsSchema>
export type UpdateThemeInput = z.infer<typeof updateThemeInputSchema>
export const settingsChannels = {
  get: 'settings:get',
  updateTheme: 'settings:update-theme',
} as const
```

## Example handler registration

```ts
// src/main/modules/settings/ipc/register-settings-ipc.ts
import { ipcMain, type BrowserWindow } from 'electron'
import { settingsChannels, settingsSchema, updateThemeInputSchema } from '../../../../shared/contracts/settings'

export function registerSettingsIpc(
  window: BrowserWindow,
  services: { getSettings(): Promise<unknown>; updateTheme(theme: 'system'|'light'|'dark'): Promise<unknown> },
  assertSender: (event: Electron.IpcMainInvokeEvent, window: BrowserWindow) => void,
) {
  ipcMain.handle(settingsChannels.get, async (event) => {
    assertSender(event, window)
    return settingsSchema.parse(await services.getSettings())
  })
  ipcMain.handle(settingsChannels.updateTheme, async (event, input: unknown) => {
    assertSender(event, window)
    const { theme } = updateThemeInputSchema.parse(input)
    return settingsSchema.parse(await services.updateTheme(theme))
  })
  return () => {
    ipcMain.removeHandler(settingsChannels.get)
    ipcMain.removeHandler(settingsChannels.updateTheme)
  }
}
```

In production, only one registration should own a channel at a time; handlers must survive recreation of authorized windows by using appropriate lifecycle-aware authorization, not a stale window reference. Handle errors with safe serializable error codes and log detailed diagnostics only in main, without secrets. Avoid leaking raw schema issues if they contain private input.

## Preload and renderer adapter

```ts
// preload example; keep the module bundled for a sandboxed preload
import { contextBridge, ipcRenderer } from 'electron'
import { settingsChannels, type Settings, type UpdateThemeInput } from '../shared/contracts/settings'

const api = {
  settings: {
    get: (): Promise<Settings> => ipcRenderer.invoke(settingsChannels.get),
    updateTheme: (value: UpdateThemeInput): Promise<Settings> =>
      ipcRenderer.invoke(settingsChannels.updateTheme, value),
  },
}
contextBridge.exposeInMainWorld('desktop', api)
export type DesktopApi = typeof api
```

```ts
// renderer: src/renderer/src/types/desktop.d.ts
import type { DesktopApi } from '../../../preload/index'
declare global { interface Window { desktop: DesktopApi } }
export {}
```

The renderer's **type-only** import is okay when bundling resolves it away; prefer emitting `DesktopApi` into `shared/contracts` if tooling accidentally pulls preload runtime code into the renderer. Do not import the preload *value* in renderer.

## Events and subscriptions

For event-like capabilities, expose a typed `subscribe(callback): () => void` that maps one named `ipcRenderer.on` listener to sanitized DTOs and returns a cleanup function. Never forward the raw `event` argument. Validate event payloads in renderer before use, and dispose on unmount/close. Add sequence IDs for meaningful ordering and resync if an event may be missed.

## Special cases

- **Long operation:** return a job ID; progress via scoped event subscription, support cancellation and bounded concurrency.
- **Binary/large data:** prefer scoped streaming or transfer mechanisms; avoid repeated huge structured-clone IPC payloads.
- **Multiple windows:** define per-window capability allowlists; validate sender window + frame, not only hostname.
- **Backward compatibility:** version contracts when persisted data, sidecars, workers, or independently released components rely on them.

Reference: https://www.electronjs.org/docs/latest/tutorial/ipc
