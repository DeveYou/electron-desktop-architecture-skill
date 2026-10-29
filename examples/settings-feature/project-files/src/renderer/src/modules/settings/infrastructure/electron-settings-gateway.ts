import type { Settings, Theme } from '../../../../../shared/contracts/settings'

/** Renderer adapter. Window typing is declared in the app's global .d.ts. */
export const electronSettingsGateway = {
  get(): Promise<Settings> { return window.desktop.settings.get() },
  updateTheme(theme: Theme): Promise<Settings> {
    return window.desktop.settings.updateTheme({ theme })
  },
}
