import type { SettingsRepository } from '../application/settings-service'
import type { Settings } from '../../../../shared/contracts/settings'

/** Test/demo adapter only. Data is lost on app restart. */
export function createInMemorySettingsRepository(
  initial: Settings = { theme: 'system' },
): SettingsRepository {
  let current = { ...initial }
  return {
    async read() { return { ...current } },
    async write(settings) { current = { ...settings } },
  }
}
