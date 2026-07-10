"""Core engine for py-modu (command: pyrun).

A Go-like runner for Python projects:
    pyrun .          -> auto-detect and run the project's entry point
    pyrun script.py  -> run a specific file
    pyrun . -- a b   -> pass "a b" through to the script's sys.argv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from subprocess import run as subprocess_run
from typing import List, Optional

__version__ = "0.1.1"

# Conventional entry-point filenames, checked in this order.
ENTRY_CANDIDATES = ("main.py", "app.py", "run.py")

# Files we never want to guess as an entry point even if they're the
# only .py file lying around.
IGNORED_NAMES = {"setup.py", "conftest.py"}


def _discover_entry(directory: Path) -> Path:
    """Resolve which file `pyrun .` should execute.

    Resolution order:
      1. A conventional entry file: main.py, app.py, run.py
      2. If exactly one non-ignored .py file exists, use it
      3. Otherwise, fail with a helpful message asking the user to be explicit
    """
    for name in ENTRY_CANDIDATES:
        candidate = directory / name
        if candidate.is_file():
            return candidate

    py_files = sorted(
        p for p in directory.glob("*.py") if p.name not in IGNORED_NAMES
    )

    if len(py_files) == 1:
        return py_files[0]

    if len(py_files) > 1:
        names = ", ".join(p.name for p in py_files)
        entry_names = "/".join(ENTRY_CANDIDATES)
        print(
            f"Error: found multiple Python files ({names}) and none is named "
            f"{entry_names}.\n"
            f"Either create one of those, or run a specific file directly:\n"
            f"    pyrun <file.py>",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Error: no Python files found in '{directory}'.", file=sys.stderr)
    sys.exit(1)


def _execute(target: Path, passthrough: List[str]) -> None:
    if not target.is_file():
        print(f"Error: '{target}' does not exist.", file=sys.stderr)
        sys.exit(1)
    if target.suffix != ".py":
        print(f"Error: '{target}' is not a .py file.", file=sys.stderr)
        sys.exit(1)

    result = subprocess_run([sys.executable, str(target), *passthrough])
    sys.exit(result.returncode)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pyrun",
        description=(
            "A Go-like runner for Python projects. "
            "Type `pyrun .` instead of `python3 script.py`."
        ),
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"pyrun {__version__}"
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="'.' for the current directory, or a path to a .py file",
    )
    parser.add_argument(
        "script_args",
        nargs=argparse.REMAINDER,
        help="Arguments passed through to the script (put a -- before them)",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.target is None:
        parser.print_help()
        sys.exit(0)

    passthrough = args.script_args
    if passthrough and passthrough[0] == "--":
        passthrough = passthrough[1:]

    if args.target == ".":
        entry = _discover_entry(Path.cwd())
    else:
        entry = Path(args.target)

    _execute(entry, passthrough)


if __name__ == "__main__":
    main()
