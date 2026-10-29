# Distribution, signing, updates, and operations

## Packaging choice

- Electron Forge has official Electron ecosystem guidance for packaging/publishing; a reasonable default when no special installer requirement exists.
- electron-builder is a widely used alternative; choose it if required installer or updater features dictate. Do **not** mix both for the same release pipeline without deliberate justification.
- Match packaging configuration to electron-vite's build outputs, assets, asar/unpacked native binaries, application identifiers, icon formats, and platform entitlements.

## Release architecture

1. Pin lockfile and CI runtime. Verify dependency licenses, SBOM policies and known vulnerabilities.
2. Build reproducibly on target operating systems/architectures where possible; OS packaging and signing may require native runners.
3. Add signing and macOS notarization for distribution as needed; store credentials in CI secrets with least privilege. Verify signed artifacts.
4. Choose explicit channels (`stable`, `beta`) and versioning strategy (SemVer or documented equivalent), with changelog and reversible migrations.
5. Implement an updates strategy *only after* selecting updater/installer distribution model. Electron's built-in updater differs by OS; Linux commonly uses platform package management.
6. Publish checksums and secure distribution URLs; never accept arbitrary update feeds or remote code execution paths.
7. Test upgrade from prior versions, new install, offline startup, interrupted update, rollback/recovery and user data integrity.
8. Crash diagnostics should be redacted and privacy-conscious. Make telemetry opt-in/opt-out as product requirements dictate; never ship sensitive user data or tokens accidentally.

## CI pipeline design

- PR: format, lint, typecheck, tests, dependency scan, production build; smoke for impacted platforms.
- Release: trusted tag/release approval, platform builds, signing/notarization, installer smoke, artifacts and provenance, staged rollout when updater supports it.
- Security: audit Electron fuses/CSP, verify permission/nav guards, review third-party scripts and native dependencies.
- Performance: detect significant regressions in cold/warm startup, memory, main-thread stalls, and large-list rendering.

## Desktop edge cases to cover

- Multiple monitors, display scale/DPI, Windows maximize/restore, macOS traffic lights, Linux WM behavior.
- Sleep/resume, network loss, filesystem changes, single-instance behavior, deep links, OS notifications, tray, external links, clipboard if used.
- Clean shutdown, handling of unsaved work, database migration failures, app restart/reload during update.

## Sources

- https://www.electronjs.org/docs/latest/tutorial/forge-overview
- https://www.electronjs.org/docs/latest/tutorial/code-signing
- https://www.electronjs.org/docs/latest/tutorial/updates
