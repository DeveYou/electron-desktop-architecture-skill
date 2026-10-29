import { ipcMain, type BrowserWindow, type IpcMainInvokeEvent } from 'electron'
import {
  settingsChannels, settingsSchema, updateThemeSchema,
} from '../../../../shared/contracts/settings'
import type { SettingsService } from '../application/settings-service'

/** Inject a guard that checks exact trusted webContents, top-level frame and app origin. */
export function registerSettingsIpc(
  authorizedWindow: BrowserWindow,
  service: SettingsService,
  assertTrustedSender: (event: IpcMainInvokeEvent, win: BrowserWindow) => void,
): () => void {
  ipcMain.handle(settingsChannels.get, async (event) => {
    try {
      assertTrustedSender(event, authorizedWindow)
      return settingsSchema.parse(await service.get())
    } catch {
      // Emit only a safe message to renderer; trusted main process may log a redacted cause.
      throw new Error('Settings request failed')
    }
  })
  ipcMain.handle(settingsChannels.updateTheme, async (event, raw: unknown) => {
    try {
      assertTrustedSender(event, authorizedWindow)
      const input = updateThemeSchema.parse(raw)
      return settingsSchema.parse(await service.updateTheme(input.theme))
    } catch {
      throw new Error('Settings update failed')
    }
  })
  return () => {
    ipcMain.removeHandler(settingsChannels.get)
    ipcMain.removeHandler(settingsChannels.updateTheme)
  }
}
