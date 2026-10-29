import { useEffect, useState } from 'react'
import type { Settings, Theme } from '../../../../../shared/contracts/settings'
import { electronSettingsGateway } from '../infrastructure/electron-settings-gateway'

/** Small hook; use an app-level query/cache strategy if the feature grows. */
export function useSettings() {
  const [settings, setSettings] = useState<Settings | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [pending, setPending] = useState(false)

  useEffect(() => {
    let active = true
    electronSettingsGateway.get()
      .then((result) => { if (active) setSettings(result) })
      .catch(() => { if (active) setError('Unable to load preferences') })
    return () => { active = false }
  }, [])

  async function updateTheme(theme: Theme) {
    if (pending) return
    setPending(true)
    setError(null)
    try { setSettings(await electronSettingsGateway.updateTheme(theme)) }
    catch { setError('Unable to save preferences') }
    finally { setPending(false) }
  }
  return { settings, error, pending, updateTheme }
}
