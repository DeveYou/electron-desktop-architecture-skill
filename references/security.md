# Electron security model (mandatory)

**Threat model:** renderer content can be compromised (XSS, malicious imported content, third-party scripts). Never trust a renderer merely because it ships with the app. Other windows/iframes may attempt IPC. External URLs, file paths, update feeds, plugins and remote HTML are untrusted inputs.

## Main window essentials

```ts
new BrowserWindow({
  webPreferences: {
    preload: join(__dirname, '../preload/index.js'), // adjust for actual build output
    contextIsolation: true,
    sandbox: true,
    nodeIntegration: false,
    webSecurity: true,
  },
})
```

**Adapt paths to electron-vite's build output; do not copy a guessed output path.** Never set `enableRemoteModule`, disable sandbox for convenience, or load arbitrary remote pages in a privileged application window. Configure sessions and app windows as a single audited security policy.

## Mandatory controls

1. **Permission requests:** deny by default with `session.setPermissionRequestHandler`; explicitly allow narrowly scoped, user-initiated capabilities after checking origin and details. Review permission checks too.
2. **CSP:** production `script-src 'self'` with restrictive `default-src`, `object-src 'none'`, `frame-src`, `connect-src`, `img-src` and style policy appropriate to the build. Use hashes/nonces if needed. Document any development-only allowances.
3. **Navigation:** prevent navigation away from trusted application URL(s), deny new windows by default with `setWindowOpenHandler`, and only open deliberately allowlisted `https:` links through `shell.openExternal` after strict URL parse + host/protocol verification.
4. **Local app protocol:** prefer a registered secure `app://` (or equivalent) custom protocol for packaged renderer assets rather than relying on `file://`; implement/register before app ready, test paths and CSP.
5. **IPC:** expose per-capability functions, never generic `send/invoke/on` nor Electron event objects; authenticate the sender webContents and top-level frame/origin; validate payload schemas, authorization and resource scope in main; throttle expensive operations where justified.
6. **Filesystem:** never allow arbitrary unvalidated paths from renderer; use user-controlled native dialog flows, scope granted file paths, validate extensions/size/content, protect against traversal and symlink escapes as needed. Use atomic writes and migrate safely.
7. **Secrets:** never expose secret tokens to renderer logs, telemetry, UI stores, or localStorage. Use secure OS facilities only after evaluating platform/signing constraints; make encryption-at-rest assumptions explicit.
8. **Storage/network:** use TLS, allowlisted endpoints, timeouts, bounded responses, dependency scanning and safe file parsing; never render untrusted HTML with unsanitized `dangerouslySetInnerHTML`.
9. **Updates:** signatures, provenance, controlled channels, test install/rollback/failure paths. Sign and notarize on macOS, and sign Windows artifacts where relevant.
10. **Fuses:** evaluate Electron fuses for production hardening; do not change fuses without validating compatibility with packaging and native dependencies.
11. **Dev tools:** avoid exposing development-only capabilities, secrets, or server endpoints to production.

## IPC sender authorization pattern

```ts
function assertTrustedSender(event: Electron.IpcMainInvokeEvent, win: Electron.BrowserWindow) {
  if (event.sender !== win.webContents ||
      event.senderFrame !== win.webContents.mainFrame) {
    throw new Error('Untrusted IPC sender')
  }
  const url = event.senderFrame?.url
  if (!url || !isApprovedApplicationUrl(url)) {
    throw new Error('Untrusted IPC origin')
  }
}
```

Implement `isApprovedApplicationUrl` with a strict, environment-specific allowlist of *exact* trusted app origin(s) and paths. Never permit any `localhost` port, any `file://` path, or any `https:` origin by wildcard. If a feature can open a new window, authorize that window and its IPC capabilities separately.

## Review checklist

- Search for `nodeIntegration: true`, `contextIsolation: false`, `sandbox: false`, `webSecurity: false`, `eval`, generic IPC bridges, `allowpopups`, unsanitized HTML, wildcard openExternal.
- Verify an untrusted renderer cannot access file system, launch programs, change global settings, or retrieve private records through forged IPC messages.
- Verify permission denials and invalid args return safe, predictable UI errors.
- Treat a scanner as **advisory**, never as proof of security.

Source: https://www.electronjs.org/docs/latest/tutorial/security/
