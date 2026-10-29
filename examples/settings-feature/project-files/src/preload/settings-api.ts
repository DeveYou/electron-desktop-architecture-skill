import { ipcRenderer } from 'electron'
import {
  settingsChannels, type Settings, type UpdateTheme,
} from '../shared/contracts/settings'

/** Merge into your single contextBridge exposure, never export generic IPC. */
export const settingsApi = {
  get: (): Promise<Settings> => ipcRenderer.invoke(settingsChannels.get),
  updateTheme: (input: UpdateTheme): Promise<Settings> =>
    ipcRenderer.invoke(settingsChannels.updateTheme, input),
}
