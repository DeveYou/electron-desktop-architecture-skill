import { z } from 'zod'

export const themeSchema = z.enum(['system', 'light', 'dark'])
export const settingsSchema = z.object({ theme: themeSchema }).strict()
export const updateThemeSchema = z.object({ theme: themeSchema }).strict()

export type Theme = z.infer<typeof themeSchema>
export type Settings = z.infer<typeof settingsSchema>
export type UpdateTheme = z.infer<typeof updateThemeSchema>

export const settingsChannels = {
  get: 'settings:get',
  updateTheme: 'settings:update-theme',
} as const
