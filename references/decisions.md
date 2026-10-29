# Architecture decision records (ADRs)

Use an ADR when a choice changes boundaries, long-term dependencies, persistence models, processes, packaging/updating, privacy, security posture, or design-system foundations.

```md
# ADR-0001: <short decision name>

- Status: Proposed | Accepted | Superseded
- Date: YYYY-MM-DD
- Decision owners: <team/role>

## Context
<problem, constraints, operational setting>

## Decision
<what was chosen and scope>

## Considered alternatives
- A: pros/cons
- B: pros/cons

## Consequences
<maintenance, performance, security, accessibility, migration cost>

## Verification
<tests, metrics, roll-back strategy>
```

Starter decisions worth recording: Electron over other runtimes, electron-vite rather than ad-hoc bundling, renderer module architecture, native persistence model, packaging/updater choice, app URL scheme, design-token convention, and telemetry/privacy policy.
