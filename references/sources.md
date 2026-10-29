# Authoritative documentation and freshness

These links are references, **not** version pins. Verify current API versions and platform limitations before implementing or releasing.

## Skill format and agent paths

- Open Agent Skills specification: https://agentskills.io/specification
- Agent Skills project: https://github.com/agentskills/agentskills
- Codex skill authoring and install: https://learn.chatgpt.com/docs/build-skills
- Claude Code user/project skill directories: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Google Antigravity App/IDE/CLI skill paths: https://antigravity.google/docs/skills
- Gemini CLI skills: https://geminicli.com/docs/cli/creating-skills/
- GitHub Copilot agent skills: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- OpenCode skills: https://docs.opencode.ai/docs/skills/

## Electron and frontend

- Electron security checklist: https://www.electronjs.org/docs/latest/tutorial/security/
- Electron IPC guide: https://www.electronjs.org/docs/latest/tutorial/ipc
- Electron process model: https://www.electronjs.org/docs/latest/tutorial/process-model
- Electron context isolation: https://www.electronjs.org/docs/latest/tutorial/context-isolation
- Electron custom protocol: https://www.electronjs.org/docs/latest/api/protocol
- electron-vite: https://electron-vite.org/guide/
- electron-vite folder conventions: https://electron-vite.org/guide/dev
- React: https://react.dev/
- Tailwind CSS: https://tailwindcss.com/docs/installation/using-vite
- shadcn/ui Vite: https://ui.shadcn.com/docs/installation/vite
- Radix primitives: https://www.radix-ui.com/primitives
- Zod: https://zod.dev/
- Zustand: https://zustand.docs.pmnd.rs/
- TanStack Query: https://tanstack.com/query/latest

## Verification and release

- Electron testing: https://www.electronjs.org/docs/latest/tutorial/automated-testing
- Playwright Electron API: https://playwright.dev/docs/api/class-electron
- Electron Forge: https://www.electronjs.org/docs/latest/tutorial/forge-overview
- Electron code signing: https://www.electronjs.org/docs/latest/tutorial/code-signing
- Electron updates: https://www.electronjs.org/docs/latest/tutorial/updates

## Freshness policy

Before creating a project or making a significant dependency change, confirm currently supported Node/Electron/Vite/React/Tailwind versions, preload bundling, native-module rebuild requirements, tooling flags, CSP behavior and installer/updater constraints in authoritative docs. If offline, label assumptions and avoid made-up commands or exact version claims.
