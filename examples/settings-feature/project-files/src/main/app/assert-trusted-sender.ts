import type { BrowserWindow, IpcMainInvokeEvent } from 'electron'

/**
 * Example guard. `approvedDevOrigin` must be the exact dev-server origin from
 * trusted startup configuration, never arbitrary renderer input. For production,
 * this example assumes a secure custom app://desktop protocol is registered.
 */
export function createSenderGuard(approvedDevOrigin?: string) {
  return (event: IpcMainInvokeEvent, win: BrowserWindow): void => {
    if (event.sender !== win.webContents ||
        event.senderFrame !== win.webContents.mainFrame) {
      throw new Error('Untrusted IPC sender')
    }
    const raw = event.senderFrame?.url
    if (!raw) throw new Error('Missing IPC origin')
    let url: URL
    try { url = new URL(raw) }
    catch { throw new Error('Invalid IPC origin') }

    const packaged = url.protocol === 'app:' && url.hostname === 'desktop'
    const dev = Boolean(approvedDevOrigin && url.origin === approvedDevOrigin)
    if (!packaged && !dev) throw new Error('Untrusted IPC origin')
  }
}
