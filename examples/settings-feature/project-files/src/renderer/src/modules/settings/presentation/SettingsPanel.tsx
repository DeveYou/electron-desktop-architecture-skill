import { useSettings } from '../application/use-settings'
import type { Theme } from '../../../../../shared/contracts/settings'

export function SettingsPanel() {
  const { settings, error, pending, updateTheme } = useSettings()
  return (
    <section aria-labelledby="settings-title" className="space-y-4 p-6">
      <h1 id="settings-title" className="text-xl font-semibold">Appearance</h1>
      {!settings && !error && <p role="status">Loading preferences…</p>}
      {error && <p role="alert" className="text-destructive">{error}</p>}
      {settings && (
        <label className="flex items-center gap-3">
          <span>Theme</span>
          <select
            value={settings.theme}
            disabled={pending}
            onChange={(e) => void updateTheme(e.target.value as Theme)}
            className="rounded-md border bg-background p-2 text-foreground"
          >
            <option value="system">System</option>
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </label>
      )}
    </section>
  )
}
