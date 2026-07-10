# Changelog

## 0.1.1 — 2026-07-10

- Simplified the CLI: `pyrun .` instead of `py run run .` (dropped the
  `run` subcommand entirely one less thing to type or remember).

- Renamed the command itself from `py` to `pyrun` to avoid clashing with
  the Windows Python Launcher (`py.exe`).

- Replaced "run whichever file was modified most recently" with explicit,
  predictable entry-point discovery: `main.py` -> `app.py` -> `run.py` ->
  the single `.py` file, in that order.

- Added argument passthrough: `pyrun . -- --flag value`.

- Moved to a `src/` package layout.

- Added `--version` flag and proper `--help` output.

- Added test suite and multi-OS/multi-Python-version CI (3.8-3.13 on
  Linux, macOS, Windows).

- Documented a one-line `pipx` bootstrap so install works the same on
  any system without prerequisites.

- Expanded docs: dedicated walkthroughs fot the pipx PATH-not-loaded-yet gotcha right after `ensurepath`, and the PEP 668 "externally-managed-environment" error on Debian/Ubuntu both are common on a fresh install, not bugs in the tool itself.


## 0.1.0
- Initial internal prototype (`py run .`), flat layout.
