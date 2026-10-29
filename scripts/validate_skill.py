#!/usr/bin/env python3
"""Minimal dependency-free Agent Skill bundle validation (not a code/security audit)."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import re
import sys

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    manifest = root / "SKILL.md"
    if not manifest.is_file():
        return [f"Missing {manifest}"]
    text = manifest.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        return ["SKILL.md must start with YAML frontmatter delimited by ---"]
    front = match.group(1)
    fields = {}
    for line in front.splitlines():
        if re.match(r"^\S[^:]*:\s*", line):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"\'')
    name = fields.get("name", "")
    desc = fields.get("description", "")
    if not NAME_RE.fullmatch(name) or len(name) > 64:
        errors.append("name must be lowercase kebab-case (max 64 chars)")
    if root.name != name:
        errors.append(f"folder name {root.name!r} must equal skill name {name!r}")
    if not (1 <= len(desc) <= 1024):
        errors.append("description must contain 1-1024 chars")
    if len(text.splitlines()) > 500:
        errors.append("SKILL.md should be <= 500 lines; move details to references")
    if not text[match.end():].strip():
        errors.append("SKILL.md body cannot be empty")
    for source in root.rglob('*.md'):
        for raw in LINK_RE.findall(source.read_text(encoding="utf-8")):
            link = raw.split('#', 1)[0]
            if not link or '://' in link or link.startswith(('mailto:', '#')):
                continue
            if not (source.parent / link).is_file():
                errors.append(f"broken relative link: {source.relative_to(root)} -> {raw}")
    for script in (root / "scripts").glob('*.py'):
        try:
            ast.parse(script.read_text(encoding='utf-8'), filename=str(script))
        except SyntaxError as exc:
            errors.append(f"invalid Python syntax: {script.name}: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default=Path(__file__).resolve().parent.parent, type=Path)
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    errors = validate(root)
    if errors:
        print("Skill validation FAILED:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS: {root.name} SKILL.md, frontmatter, local Markdown links and Python syntax")
    return 0


if __name__ == "__main__":
    sys.exit(main())
