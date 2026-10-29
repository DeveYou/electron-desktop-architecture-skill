#!/usr/bin/env python3
"""Install this portable skill for selected agents. Never overwrites without --force."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys
import tempfile


GLOBAL = {
    'codex': Path('~/.agents/skills'),
    'claude': Path('~/.claude/skills'),
    'antigravity': Path('~/.gemini/config/skills'),
    'antigravity-cli': Path('~/.gemini/antigravity-cli/skills'),
    'gemini-cli': Path('~/.gemini/skills'),
    'copilot': Path('~/.copilot/skills'),
    'opencode': Path('~/.config/opencode/skills'),
}
PROJECT = {
    'codex': Path('.agents/skills'),
    'claude': Path('.claude/skills'),
    'antigravity': Path('.agents/skills'),
    'antigravity-cli': Path('.agents/skills'),
    'gemini-cli': Path('.agents/skills'),
    'copilot': Path('.agents/skills'),
    'opencode': Path('.agents/skills'),
    'generic': Path('.agents/skills'),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent', choices=[*GLOBAL.keys(), 'generic'], required=True)
    parser.add_argument('--scope', choices=['global', 'project'], default='global')
    parser.add_argument('--project', type=Path, default=Path.cwd(), help='Repository root for project scope')
    parser.add_argument('--destination', type=Path, help='Override the parent skills directory')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--force', action='store_true', help='Replace existing installed copy only if explicitly requested')
    args = parser.parse_args()

    source = Path(__file__).resolve().parent.parent
    if not (source / 'SKILL.md').is_file():
        parser.error('skill source SKILL.md is missing')

    if args.destination:
        parent = args.destination.expanduser().resolve()
    elif args.scope == 'global':
        if args.agent == 'generic':
            parser.error('generic/global requires --destination because agent paths differ')
        parent = GLOBAL[args.agent].expanduser().resolve()
    else:
        project = args.project.expanduser().resolve()
        if not project.is_dir():
            parser.error(f'project does not exist: {project}')
        parent = (project / PROJECT[args.agent]).resolve()
    target = parent / source.name
    if target == source or parent == source or source in parent.parents:
        parser.error('destination must be outside the source skill folder')
    print(f'Agent: {args.agent}; scope: {args.scope}')
    print(f'Source: {source}')
    print(f'Target: {target}')
    if target.exists() and not args.force:
        print('Refusing to replace an existing skill. Use --force only after reviewing changes.', file=sys.stderr)
        return 2
    if args.dry_run:
        print('DRY RUN: no files changed')
        return 0
    parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink() or (target.exists() and not target.is_dir()):
        print('Refusing to replace a non-directory or symlink target.', file=sys.stderr)
        return 2
    # Stage on the same filesystem and preserve a previous installation on failure.
    with tempfile.TemporaryDirectory(prefix='.skill-install-', dir=parent) as staging:
        temp_root = Path(staging)
        staged = temp_root / source.name
        backup = temp_root / 'previous-installation'
        shutil.copytree(source, staged, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
        if target.exists():
            target.rename(backup)
        try:
            staged.rename(target)
        except OSError:
            if backup.exists() and not target.exists():
                backup.rename(target)
            raise
    print('Installed. Confirm agent skill discovery or restart agent session if needed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
