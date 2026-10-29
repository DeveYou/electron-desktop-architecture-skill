#!/usr/bin/env python3
"""Generate a small renderer feature module. Add native scaffolds only with --native."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

NAME = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


def pascal(value: str) -> str:
    return ''.join(word[:1].upper() + word[1:] for word in value.split('-'))


def generate(project: Path, name: str, native: bool) -> dict[Path, str]:
    feature = pascal(name)
    base = Path('src/renderer/src/modules') / name
    result = {
        base / 'index.ts': f"export {{ {feature}Page }} from './presentation/{feature}Page'\n",
        base / f'presentation/{feature}Page.tsx': (
            f"/** {feature} presentation; move behavior into application use cases. */\n"
            f"export function {feature}Page() {{\n"
            f"  return <main aria-labelledby=\"{name}-title\" className=\"p-6\">\n"
            f"    <h1 id=\"{name}-title\" className=\"text-2xl font-semibold\">{feature}</h1>\n"
            f"  </main>\n"
            f"}}\n"
        ),
        base / 'README.md': (
            f"# {feature} module\n\n"
            "Owns this feature's UI, application behavior, and domain concepts.\n\n"
            "- `index.ts` is the only public import boundary for other modules.\n"
            "- Add `domain/` when invariants exist, `application/` for use cases, and "
            "`infrastructure/` for adapter implementations. Do not create empty layers.\n"
            "- Cross to main only via a named preload capability and shared runtime-validated contract.\n"
            "- Add unit/component tests and accessible loading, error and empty states.\n"
        ),
    }
    if native:
        result.update({
            Path('src/main/modules') / name / 'README.md': (
                f"# {feature} main module\n\n"
                "Add application use cases and infrastructure adapters only for privileged capabilities.\n"
                "Register IPC in the main composition root with sender/origin checks, runtime schema validation,\n"
                "and authorization. Never expose a generic ipcRenderer bridge.\n"
            ),
            Path('src/shared/contracts') / f'{name}.ts': (
                f"// {feature} serializable IPC contract placeholder.\n"
                "// Define runtime DTO schemas (e.g. Zod), explicit channel IDs, and inferred TypeScript types.\n"
                "// No React, Electron, Node, storage, or secrets here.\n"
                "export {}\n"
            ),
        })
    return {project / path: contents for path, contents in result.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--name', required=True, help='lowercase kebab-case module name')
    parser.add_argument('--native', action='store_true', help='Also create main and shared IPC placeholders')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if not NAME.fullmatch(args.name):
        parser.error('name must be lower-case kebab-case, e.g. activity-feed')
    root = args.project.expanduser().resolve()
    if not root.is_dir() or not (root / 'src/renderer/src').is_dir():
        parser.error('project must exist and contain src/renderer/src (electron-vite convention)')
    files = generate(root, args.name, args.native)
    collision = [str(f) for f in files if f.exists()]
    if collision:
        print('Refusing to overwrite existing files:', *collision, sep='\n - ', file=sys.stderr)
        return 2
    for path in files:
        print(f'{"Would create" if args.dry_run else "Create"}: {path.relative_to(root)}')
    if args.dry_run:
        return 0
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    print('Module scaffold created. Fill in domain/use cases/adapters as required; add tests.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
