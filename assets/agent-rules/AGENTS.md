# Engineering guidelines for AI agents

When building or modifying this Electron desktop application, use the `electron-desktop-architecture` Agent Skill installed in your skills directory (or read `.agents/skills/electron-desktop-architecture/SKILL.md` when checked into this repository).

- Preserve the existing application architecture and follow module public APIs.
- Electron main owns privileged operations; preload exposes only narrow, typed methods; React renderer never imports Electron or Node runtime APIs.
- Treat IPC as a security boundary; validate sender, payload, and authorization in main.
- Keep domain/application code framework-independent; use feature modules and semantic design tokens.
- Always add suitable unit/component/IPC tests and report actual verification results.
- Read task-specific skill references on demand, rather than copying all guidance into this file.
