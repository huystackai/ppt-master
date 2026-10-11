#!/usr/bin/env python3
"""
PPT Master - Standalone Skill Packager

Package the complete root skill, including the example gallery, with a checksum
inventory. Exclude runtime credentials, private projects, caches and Git metadata.

Usage:
    python3 scripts/package_skill.py [-o <archive.zip>]

Examples:
    python3 scripts/package_skill.py
    python3 scripts/package_skill.py -o dist/ppt-master-skill.zip

Dependencies:
    None (only uses the Python standard library).
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import sys
import zipfile
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
ROOT_FILES = (
    'SKILL.md', 'README.md', 'README_CN.md', 'AGENTS.md', 'CLAUDE.md',
    'LICENSE', 'CODE_OF_CONDUCT.md', 'CONTRIBUTING.md', 'SECURITY.md',
    'requirements.txt', '.env.example', '.gitignore', 'index.html', 'viewer.html',
    'projects/README.md',
)
RESOURCE_DIRS = ('agents', 'scripts', 'references', 'workflows', 'templates', 'docs', 'examples', '.claude-plugin', '.github')
PRIVATE_DIRS = {'.git', '.venv', 'venv', '__pycache__', 'node_modules', '.cache', '.preview', '.review'}
PRIVATE_FILES = (
    '.DS_Store', '._*', '*.pyc', '*.pyo', '*.log', '*.tmp', '*.bak',
    'credentials*.json', 'service-account*.json', 'secrets*.json', '*.pem', '*.p12', '*.pfx',
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Build the complete portable PPT Master skill ZIP.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('-o', '--output', type=Path, default=SKILL_DIR / 'dist/ppt-master-skill.zip')
    return parser


def shareable(path: Path) -> bool:
    """Keep packaged resources free of runtime and authentication artifacts."""
    relative = path.relative_to(SKILL_DIR)
    if set(relative.parts) & PRIVATE_DIRS:
        return False
    if path.name.startswith('.env') and path.name != '.env.example':
        return False
    return not any(fnmatch.fnmatch(path.name, pattern) for pattern in PRIVATE_FILES)


def collect_files() -> list[Path]:
    """Collect every feature resource using explicit top-level package boundaries."""
    files = [SKILL_DIR / name for name in ROOT_FILES]
    for name in RESOURCE_DIRS:
        directory = SKILL_DIR / name
        if not directory.is_dir():
            raise RuntimeError(f'Missing feature directory: {name}. Restore it before packaging.')
        files.extend(p for p in directory.rglob('*') if p.is_file() and shareable(p))
    for path in files:
        if not path.is_file():
            raise RuntimeError(f'Missing package file: {path.relative_to(SKILL_DIR)}')
        if path.is_symlink():
            raise RuntimeError(f'Symlinks are not portable package resources: {path.relative_to(SKILL_DIR)}')
    return sorted(set(files))


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output = args.output.expanduser().resolve()
    try:
        files = collect_files()
        if output in files:
            raise RuntimeError('Choose an archive location outside the packaged resource directories.')
        output.parent.mkdir(parents=True, exist_ok=True)
        inventory = {}
        with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            for path in files:
                relative = path.relative_to(SKILL_DIR).as_posix()
                data = path.read_bytes()
                inventory[relative] = hashlib.sha256(data).hexdigest()
                archive.write(path, 'ppt-master/' + relative)
            manifest = {
                'skill': 'ppt-master',
                'entrypoint': 'SKILL.md',
                'features': list(RESOURCE_DIRS),
                'file_count': len(files),
                'sha256': inventory,
            }
            archive.writestr('ppt-master/package_manifest.json', json.dumps(manifest, indent=2) + '\n')
        print(json.dumps({'archive': str(output), 'files': len(files), 'bytes': output.stat().st_size}))
        return 0
    except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
        print(f'Packaging failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
