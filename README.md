# Electron Desktop Architecture Skill

A reusable, vendor-neutral **Agent Skill** for building robust desktop applications with Electron + React + TypeScript. The skill is a **structural and procedural guide**, not an already running full app starter. It contains practical examples, a module generator, a validation helper, installation tooling, and optional agent instruction templates.

**Core philosophy:** modular monolith + clean inward dependencies + vertical features + typed/validated IPC + a semantic, accessible design system. Prefer lightweight layers when a feature is simple.

## Package contents

- `SKILL.md` — portable open Agent Skills manifest and task workflow; kept short for progressive loading.
- `references/` — stack policy, complete folder structure, module contracts, security, IPC, design tokens, data ownership, tests, release, decision records, and source links.
- `examples/settings-feature/` — vertical-slice settings example covering contracts, main, preload, renderer adapter, UI, and testing notes. It is **illustrative**, not a standalone compiled application.
- `assets/agent-rules/` — optional *thin* root `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` templates for projects.
- `scripts/` — cross-platform, Python 3.9+ helpers with no third-party dependencies.

## Install

Unzip so the folder `electron-desktop-architecture/` contains `SKILL.md`. Copy that **entire** folder to your agent's skills directory. Or from the extracted folder:

```bash
python3 scripts/install_skill.py --agent codex --scope global --dry-run
python3 scripts/install_skill.py --agent codex --scope global
```

For other targets:

| Agent | Global user skill directory | Project skill directory |
| --- | --- | --- |
| OpenAI Codex | `~/.agents/skills/` | `<repo>/.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `<repo>/.claude/skills/` |
| Google Antigravity App / IDE | `~/.gemini/config/skills/` | `<repo>/.agents/skills/` |
| Google Antigravity CLI | `~/.gemini/antigravity-cli/skills/` | `<repo>/.agents/skills/` |
| Google Gemini CLI | `~/.gemini/skills/` | `<repo>/.agents/skills/` |
| GitHub Copilot | `~/.copilot/skills/` | `<repo>/.agents/skills/` |
| OpenCode | `~/.config/opencode/skills/` | `<repo>/.agents/skills/` |
| Other agents supporting Agent Skills | Check the agent's supported skill path | Prefer `.agents/skills/` when supported |

Examples:

```bash
python3 scripts/install_skill.py --agent claude --scope global
python3 scripts/install_skill.py --agent antigravity --scope project --project /path/to/repo
python3 scripts/install_skill.py --agent antigravity-cli --scope global
python3 scripts/install_skill.py --agent gemini-cli --scope global
python3 scripts/install_skill.py --agent copilot --scope global
python3 scripts/install_skill.py --agent opencode --scope global
python3 scripts/install_skill.py --agent generic --destination /absolute/path/to/skills
```

The installer refuses to overwrite an existing skill unless `--force` is explicitly given. It never writes optional repository rule files automatically. The same `SKILL.md` cannot **guarantee** support on every agent; use `AGENTS.md` or equivalents as a fallback when skill discovery is unavailable.

## Use with an agent

Examples of tasks:

> Use the electron-desktop-architecture skill to scaffold a cross-platform desktop app for project management, with an accessible dark/light shell and a Settings module.

> Apply the electron-desktop-architecture skill to add a local document library module with schema-validated IPC and a native file picker.

> Audit our Electron app against the skill's process isolation, module boundaries, design tokens, and testing checklist. Do not rewrite unrelated code.

## Stack defaults

Electron + electron-vite, React, TypeScript strict mode, Tailwind CSS, shadcn/ui + Radix primitives, Lucide, Vitest + Testing Library. Use Zustand for shared ephemeral client state, TanStack Query for remote cache/server state, Zod for boundary validation. Electron Forge or electron-builder for distribution, selected explicitly. SQLite only if the product requires structured local persistence. No forced cloud backend.

## Quick module scaffold

```bash
python3 scripts/new_module.py --project /path/to/electron-project --name activity-feed --dry-run
python3 scripts/new_module.py --project /path/to/electron-project --name activity-feed
```

The scaffold creates a renderer feature boundary and short TODOs. Add main-process code and IPC only when the capability actually needs it. `--native` adds empty, documented locations for native adapters and shared contracts.

## Portability and verification

This is a framework-independent skill format; the **application target** is Electron. Any compatible agent can use the instructions. Some agents need explicit invocation or a restart to discover newly installed skills. Read `references/sources.md` for official docs and version-sensitive decisions. Do not treat included snippets as proof of a running app.

## License

MIT; see `LICENSE`.

## Offline validation

From the extracted skill directory:

```bash
python3 scripts/validate_skill.py .
python3 -m unittest discover -s tests
python3 scripts/check_boundaries.py /path/to/electron-project
```

`check_boundaries.py` is deliberately a **simple heuristic**, not a replacement for ESLint, dependency-cruiser, code review, Electron security guidance, or runtime tests.

On Windows, replace `python3` with `py -3` if that is your configured Python launcher. No Python package installations are required to install or validate this skill. For native application scaffolding and release builds, you will separately need an appropriate Node.js toolchain and OS-specific packaging dependencies.
