import { settingsSchema, type Settings, type Theme } from '../../../../shared/contracts/settings'

export interface SettingsRepository {
  read(): Promise<Settings>
  write(value: Settings): Promise<void>
}

export function createSettingsService(repository: SettingsRepository) {
  return {
    async get(): Promise<Settings> {
      return settingsSchema.parse(await repository.read())
    },
    async updateTheme(theme: Theme): Promise<Settings> {
      const current = await repository.read()
      const next = settingsSchema.parse({ ...current, theme })
      await repository.write(next)
      return next
    },
  }
}
export type SettingsService = ReturnType<typeof createSettingsService>
