#!/usr/bin/env python3
"""
PPT Master - Portable Runtime Setup

Prepare a cached Python environment for a copied or Git-installed agent skill.
Print the interpreter and capability status as JSON; keep installation logs on stderr.
See SKILL.md, Portable Agent Setup, for the agent handoff.

Usage:
    python3 scripts/bootstrap.py [--check] [--browser]

Examples:
    python3 scripts/bootstrap.py
    python3 scripts/bootstrap.py --check
    python3 scripts/bootstrap.py --browser

Dependencies:
    Python 3.10+ and its standard library; installs requirements.txt on first use.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
REQUIREMENTS = SKILL_DIR / 'requirements.txt'


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Prepare the portable PPT Master Python runtime.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--check', action='store_true', help='Report status without installing anything.')
    parser.add_argument('--browser', action='store_true', help='Also prepare Chromium for visual review.')
    return parser


def compatible_python() -> list[str] | None:
    """Find a supported Python when the default python3 is too old."""
    candidates = [[name] for name in ('python3.14', 'python3.13', 'python3.12', 'python3.11', 'python3.10', 'python')]
    if os.name == 'nt':
        candidates.insert(0, ['py', '-3'])
    for command in candidates:
        if not shutil.which(command[0]):
            continue
        result = subprocess.run(
            command + ['-c', 'import sys; raise SystemExit(sys.version_info < (3, 10))'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if result.returncode == 0:
            return command
    return None


def runtime_directory(digest: str) -> Path:
    """Locate writable runtime storage outside the installed skill."""
    override = os.environ.get('PPT_MASTER_RUNTIME_DIR')
    if override:
        return Path(override).expanduser().resolve()
    cache = Path(os.environ.get('XDG_CACHE_HOME', str(Path.home() / '.cache'))).expanduser()
    version = f'py{sys.version_info.major}{sys.version_info.minor}'
    return cache / 'ppt-master' / f'{version}-{digest[:12]}'


def run_setup(command: list[str]) -> None:
    """Run an installation command with all diagnostics on stderr."""
    subprocess.run(command, check=True, stdout=sys.stderr, stderr=sys.stderr)


def installed_requirements(python: Path) -> bool:
    """Check that the runtime still contains every declared distribution."""
    if not python.is_file():
        return False
    probe = (
        'import importlib.metadata as m, pathlib, re, sys; '
        'lines=pathlib.Path(sys.argv[1]).read_text().splitlines(); '
        'names=[re.split(r"[<>=!~;\\[]", line.strip())[0].strip() '
        'for line in lines if line.strip() and not line.lstrip().startswith("#")]; '
        '[m.version(name) for name in names]'
    )
    return subprocess.run(
        [str(python), '-c', probe, str(REQUIREMENTS)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0


def browser_ready(python: Path) -> bool:
    """Check Chromium by launching it without contacting an external service."""
    probe = (
        'from playwright.sync_api import sync_playwright; '
        'p=sync_playwright().start(); b=p.chromium.launch(headless=True); b.close(); p.stop()'
    )
    return subprocess.run(
        [str(python), '-c', probe],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    args = build_parser().parse_args(arguments)
    if sys.version_info < (3, 10):
        command = compatible_python()
        if command:
            return subprocess.call(command + [str(Path(__file__).resolve())] + arguments)
        print('Python 3.10+ is required. Install it and rerun scripts/bootstrap.py.', file=sys.stderr)
        return 1

    try:
        digest = hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()
        runtime = runtime_directory(digest)
        python = runtime / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
        stamp = runtime / '.ppt-master-requirements.sha256'
        ready = stamp.is_file() and stamp.read_text().strip() == digest and installed_requirements(python)
        if not ready and not args.check:
            print('Preparing PPT Master dependencies in the user cache...', file=sys.stderr)
            venv.EnvBuilder(with_pip=True).create(runtime)
            run_setup([str(python), '-m', 'pip', 'install', '-r', str(REQUIREMENTS)])
            run_setup([str(python), '-m', 'pip', 'check'])
            ready = installed_requirements(python)
            if not ready:
                raise RuntimeError('Dependency installation is incomplete. Rerun scripts/bootstrap.py with network access.')
            stamp.write_text(digest + '\n')

        chromium = browser_ready(python) if ready and args.browser else None
        if ready and args.browser and not chromium and not args.check:
            run_setup([str(python), '-m', 'playwright', 'install', 'chromium'])
            chromium = browser_ready(python)
            if not chromium:
                raise RuntimeError(
                    'Chromium could not launch. Install the OS libraries listed by Playwright, '
                    'then rerun scripts/bootstrap.py --browser.'
                )

        result = {
            'ready': ready and (chromium is not False),
            'python': str(python),
            'skill_dir': str(SKILL_DIR),
            'workspace': str(Path.cwd()),
            'chromium_ready': chromium,
            'external_tools': {name: bool(shutil.which(name)) for name in ('pandoc', 'ffmpeg', 'node', 'pdftoppm')},
        }
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result['ready'] else 1
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f'PPT Master setup failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
