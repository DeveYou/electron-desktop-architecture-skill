# Desktop design system: cohesive, accessible, themeable

## Principle

A "modern" UI is a consistent system, not a particular library. Build an **app shell**, tokens, primitives, patterns, and compositional modules. shadcn/ui code is owned by the app; changes to base components require design-system review. Prefer native platform behavior where familiarity/accessibility matters; customize window chrome only with explicit requirements and OS testing.

## Layering

```text
Foundations (color, type, space, radius, motion, elevation)
    ↓
Primitives (Button, Input, Dialog, Menu, Tooltip, ScrollArea)
    ↓
Patterns (AppSidebar, Toolbar, SplitPanel, EmptyState, DataTable)
    ↓
Feature compositions (LibraryList, PlayerBar, ChatThread)
    ↓
App shell + navigation
```

- **Foundations** are CSS variables and documented usage rules, never hard-coded branded hex scattered through components.
- **Primitives** are built on accessible semantics (Radix/shadcn where suitable) and accept a small, stable variant API.
- **Patterns** handle reusable product-level desktop behaviors (sidebars, resizable panels, command palette) without feature domain logic.
- **Feature components** live inside their feature module, not `shared/ui`.

## Semantic token design

Name tokens by **role**, not raw color: `background`, `foreground`, `surface`, `surface-raised`, `surface-hover`, `border`, `border-strong`, `accent`, `accent-foreground`, `muted`, `muted-foreground`, `danger`, `focus-ring`, plus charts/status variants as justified. Keep WCAG contrast requirements and disabled states in both themes.

A minimal Tailwind CSS v4-style extension (adapt to the installed shadcn version):

```css
/* src/renderer/src/app/styles/theme.css */
@import "tailwindcss";

:root {
  color-scheme: light;
  --app-bg: oklch(0.985 0.003 265);
  --app-fg: oklch(0.22 0.02 265);
  --app-surface: oklch(1 0 0);
  --app-border: oklch(0.90 0.01 265);
  --app-accent: oklch(0.55 0.20 260);
  --app-focus: oklch(0.61 0.17 260);
  --app-radius: 0.65rem;
}

.dark {
  color-scheme: dark;
  --app-bg: oklch(0.16 0.015 265);
  --app-fg: oklch(0.95 0.008 265);
  --app-surface: oklch(0.20 0.015 265);
  --app-border: oklch(0.31 0.015 265);
  --app-accent: oklch(0.72 0.15 260);
  --app-focus: oklch(0.77 0.14 260);
}

@theme inline {
  --color-app-bg: var(--app-bg);
  --color-app-fg: var(--app-fg);
  --color-app-surface: var(--app-surface);
  --color-app-border: var(--app-border);
  --color-app-accent: var(--app-accent);
  --color-app-focus: var(--app-focus);
  --radius-app: var(--app-radius);
}
```

This snippet illustrates token direction; integrate with the **actual** shadcn token convention to avoid a duplicated token system. Validate text/icon/focus contrast in real rendered combinations. Use `rem` for text/spacing so OS font scaling works. Avoid magic spacing and uncontrolled z-index values.

## Desktop app shell

- **Titlebar/drag:** macOS traffic lights, Windows window controls, maximized states, Linux window manager differences. Drag regions must not swallow buttons, inputs, or interactive controls. Native titlebars are the safe default.
- **Layout:** collapsible navigation rail/sidebar, content viewport, optional secondary inspector. Decide breakpoints based on **window width**, not smartphone screen sizes. Support minimum window size and 200% zoom.
- **Interaction:** discoverable hover, keyboard focus, command palette, right-click menus when useful, selection state, undo for destructive actions, consistent loading and empty states.
- **Scrolling:** one clear scroll owner per pane, keyboard reachable overflow, sticky controls only when justified.
- **Typography:** small coherent scale, accessible body text; don't shrink information density to the point of unusability. Use system UI font or bundled licensed fonts.
- **Motion:** 120–240ms subtle transitions only as a starting point; respect `prefers-reduced-motion` and avoid animating all properties. Prefer performance-friendly transforms/opacity.
- **Accessibility:** tab order, escape/focus trapping, visible `:focus-visible`, screen-reader labels, high contrast, errors announced, skip/bypass affordances where helpful.
- **Localization:** accommodate long strings, RTL if relevant, system locale/date/time preferences, and keyboard layout variations.

## shadcn/ui policy

1. Select a coherent base style and CSS variable naming convention at project creation.
2. Add only components actually needed. Customize via variants and tokens, not repetitive per-call arbitrary overrides.
3. Do not modify a shared primitive for one feature-specific look; compose/wrap it in that feature.
4. Always test hover, active, pressed, disabled, loading, focus, keyboard, screen reader, and both theme variants.
5. Avoid enforcing pixel-perfect copies of third-party branded UIs. Learn from their information hierarchy and interaction patterns while maintaining product identity.

## Design acceptance checklist

- Visual hierarchy is readable at 100% and 200% scaling, across narrow and wide windows.
- Window controls and context menus work on supported platforms.
- Keyboard-only path completes the main workflow.
- Themes have no un-tokenized components, contrast failures, or unreadable empty/error states.
- Animation does not convey the only signal and honors reduced motion.
- Lists with large item counts use virtualized rendering after profiling warrants it.
