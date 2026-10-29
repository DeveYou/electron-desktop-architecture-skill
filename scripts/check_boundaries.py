#!/usr/bin/env python3
"""Advisory static guard for obvious Electron boundary mistakes; not a security audit."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

IMPORT_RE = re.compile(r"(?:import|from|require\()\s*(?:[\w\s{},*]+\s+from\s*)?['\"]([^'\"]+)['\"]")
DANGERS = [
    (re.compile(r'nodeIntegration\s*:\s*true'), 'nodeIntegration enabled'),
    (re.compile(r'contextIsolation\s*:\s*false'), 'contextIsolation disabled'),
    (re.compile(r'sandbox\s*:\s*false'), 'renderer sandbox disabled'),
    (re.compile(r'webSecurity\s*:\s*false'), 'webSecurity disabled'),
    (re.compile(r'allowRunningInsecureContent\s*:\s*true'), 'insecure content enabled'),
]


def scan(project: Path) -> list[str]:
    src = project / 'src'
    problems = []
    for file in [*src.rglob('*.ts'), *src.rglob('*.tsx')]:
        rel = file.relative_to(project).as_posix()
        text = file.read_text(encoding='utf-8', errors='replace')
        is_renderer = rel.startswith('src/renderer/')
        is_shared = rel.startswith('src/shared/')
        if is_renderer or is_shared:
            for match in IMPORT_RE.finditer(text):
                imp = match.group(1)
                if imp in ('electron', 'electron/main', 'electron/renderer') or imp.startswith('node:'):
                    problems.append(f'{rel}: forbidden runtime import {imp!r} in renderer/shared')
                if is_renderer and re.search(r'(?:^|/)main/(?:modules|app)/', imp):
                    problems.append(f'{rel}: likely main-process import {imp!r}')
        for pattern, message in DANGERS:
            if pattern.search(text):
                problems.append(f'{rel}: suspicious security setting: {message}')
        if rel.startswith('src/preload/') and re.search(r'contextBridge\.exposeInMainWorld\([^\n]*ipcRenderer', text):
            problems.append(f'{rel}: possible raw ipcRenderer exposure')
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path, help='Electron project root')
    args = parser.parse_args()
    root = args.project.expanduser().resolve()
    if not (root / 'src').is_dir():
        parser.error('project must contain src/')
    findings = scan(root)
    if findings:
        print('ADVISORY FINDINGS (review manually):')
        for msg in findings: print(' -', msg)
        return 1
    print('PASS: no basic suspicious patterns found (NOT a guarantee of security)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
