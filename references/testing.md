# Testing and quality gates

## Test pyramid by risk

| Layer | Tool | Minimum tests |
| --- | --- | --- |
| Domain | Vitest | rules, validation, invariants, edge cases |
| Application | Vitest + injected fakes | use-case success/error, cancellation, side effects |
| Main adapters + IPC | Vitest/integration with Electron-aware harness | schema failure, untrusted sender, denied resource, safe error translation |
| Renderer | React Testing Library + user-event | accessible interactions, loading/empty/error/success |
| Design-system | Storybook (optional) + accessibility audit | focus/keyboard/theme/contrast/variants |
| End to end | Playwright Electron (experimental Electron integration) or WebdriverIO | launch, primary workflow, native integration, restart/persistence, packaging smoke |

## Required CI gates

```text
format-check → lint → typecheck → unit/component tests
                            ↓
                        production build
                            ↓
                 platform smoke tests / security review
                            ↓
                    signed release (when configured)
```

- Always run `npm run typecheck` / `lint` / `test` / `build` when these scripts exist; if not, note which scripts are absent rather than falsely claiming verification.
- Use fixture data and fake adapters to test use cases without starting Electron.
- Test trusted sender and schema validation separately; an IPC handler is a security boundary, not just a function.
- Verify client-side boundaries with `eslint-plugin-boundaries`, `dependency-cruiser`, or an equivalent import graph rule; check `main`, `preload`, `renderer`, and `shared` are not coupled backwards.
- For visual regression, capture deliberate baselines at fixed viewport, theme, platform, and font settings; verify manually before accepting snapshots.
- End-to-end cross-platform smoke should cover fresh install, start, resume, settings persistence, deep links if used, updates if used, window controls, installer integrity, and uninstall policies.
- Beware that Playwright's Electron support is documented as experimental; keep E2E details under review with upgrades.

## Example acceptance matrix

```text
[ ] Core use case tested independently of UI and Electron
[ ] Schema rejects malformed native IPC input
[ ] Untrusted renderer/frame cannot invoke privileged handler
[ ] Renderer handles pending/empty/error/success states
[ ] Navigation uses keyboard; focus remains visible
[ ] macOS/Windows/Linux behavior tested or not-tested reported
[ ] No renderer import of electron/node: modules
[ ] No direct cross-feature imports from internal directories
[ ] Build succeeds; packaging tested when relevant
```

## Reporting

Final agent response should include: changed files/features, architecture and threat-model decisions, commands executed with pass/fail, not-run checks, notable tradeoffs, and remaining issues. Do not report hypothetical tests as passed.

## Bundled helper checks

```bash
python3 scripts/validate_skill.py .
python3 -m unittest discover -s tests
python3 scripts/check_boundaries.py /path/to/electron-project
```

The bundled boundary scanner is a quick heuristic only; import graph tools, manual code review and actual Electron tests remain essential.
