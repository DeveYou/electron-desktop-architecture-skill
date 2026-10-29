import { contextBridge } from 'electron'
import { settingsApi } from './settings-api'

/** App-wide bridge: merge additional *named* capabilities here. */
const desktopApi = { settings: settingsApi }
contextBridge.exposeInMainWorld('desktop', desktopApi)
export type DesktopApi = typeof desktopApi
