# py-modu

A Go-like CLI runner for Python projects.

In Go, you run a project with `go run .`. In Python, you're stuck typing
`python3 the_exact_filename.py` every time. `py-modu` gives Python the same
convenience: type `pyrun .` and it figures out what to execute.

```bash
pyrun .
```

## Installation

### Recommended: pipx (isolated, global, no system conflicts)

```bash
pipx install py-modu
```

[pipx](https://pypa.github.io/pipx/) installs CLI tools into their own
isolated environment and puts them on your `PATH`, so `pyrun` is available
everywhere without touching your system Python or any project's virtualenv.

Don't have `pipx` yet? One line gets you both, on any OS:

```bash
python3 -m pip install --user pipx && python3 -m pipx ensurepath
```

(Windows: use `py -m pip install --user pipx` then `py -m pipx ensurepath`
in PowerShell, then restart the terminal so the updated `PATH` takes
effect.)

### Alternative: pip

```bash
pip install py-modu
```

On some Linux distributions, installing CLI tools system-wide with plain
`pip` is blocked (PEP 668, "externally-managed-environment"). If you hit
that, use `pipx` instead, or install into a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate      # .venv\Scripts\activate on Windows
pip install py-modu
```

`py-modu` works on **Python 3.8 and newer**, on Linux, macOS, and Windows.

## Usage

```bash
# Run the current project. py-modu looks for, in order:
#   1. main.py
#   2. app.py
#   3. run.py
#   4. the single .py file in the directory, if there's only one
pyrun .

# Run a specific file
pyrun path/to/script.py

# Pass arguments through to your script's sys.argv
pyrun . -- --input data.csv --verbose

# Check the installed version
pyrun --version
```

If `pyrun .` finds more than one `.py` file and none of them is named
`main.py`, `app.py`, or `run.py`, it will ask you to either rename one of
them or run the target file explicitly — it will never silently guess.

## Why not just use `python3 script.py`?

You still can `py-modu` doesn't replace anything, it just removes the
need to remember or type the exact entry-point filename, the same way
`go run .` does for Go projects. It's a small quality-of-life tool for
people who bounce between a lot of small Python scripts and projects.

## Development

```bash
git clone https://github.com/maxchichar/py-modu.git
cd py-modu
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## License

MIT — see [LICENSE](LICENSE).
