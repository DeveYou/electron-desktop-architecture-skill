# Module contract and feature lifecycle

## Module design card (write before implementing)

```yaml
name: settings
purpose: Own user-editable appearance and application preferences
processes: [renderer, main]
public_api: [SettingsPage, useSettings]
domain: [ThemePreference, Settings]
commands: [getSettings, updateTheme]
events: [settingsChanged]
ports: [SettingsRepository]
state_owner: main settings service
persisted_data: [theme]
permissions: [none]
error_cases: [invalid_theme, storage_failure]
tests: [domain, ipc, renderer, end_to_end]
```

## Change workflow

1. Define one concrete user story, acceptance criteria, platform caveats, and accessibility requirements.
2. Draw data flow: command origin → renderer adapter → preload → handler → use case → persistence. Name any events and the owner of each.
3. Introduce schemas/contracts in `src/shared/contracts/<feature>.ts` for crossings only. Avoid runtime validators for internal pure functions without a threat boundary.
4. Implement use case and ports with unit tests; then persistence adapter; then authorized, schema-validating main IPC handlers; then preload; then renderer adapter/hook; then UI.
5. Export only what consumers require from each module's `index.ts`. No cross-feature deep imports.
6. Integrate in composition root and navigation; add lifecycle disposal for handlers/events.
7. Test happy, invalid, canceled, untrusted sender, denied permission, persistence failure, cross-platform behavior, and accessibility.

## Cross-module collaboration

- First preference: one application-level orchestrator calls public interfaces of two modules.
- Second: typed event subscription for one-to-many state-change notifications where consistency model is documented.
- Avoid: feature A writing feature B's database table, importing its internal repository, or dispatching untyped string events via a global bus.

## Definition of done

- Feature is independently understandable, tested and observable.
- Public API and contract changes documented; runtime data is validated at trust boundaries.
- User receives accessible loading/error/empty/success states.
- Side effects are cleaned up and errors do not reveal sensitive stack traces through IPC.
- Package builds and smoke test works in target environment(s).
