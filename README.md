# py-modu

[![PyPI version](https://img.shields.io/pypi/v/py-modu.svg)](https://pypi.org/project/py-modu/)
[![Python versions](https://img.shields.io/pypi/pyversions/py-modu.svg)](https://pypi.org/project/py-modu/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A Go-like CLI runner for Python projects.

In Go, you run a project with `go run .`. In Python, you're stuck typing
`python3 the_exact_filename.py` every time and remembering that filename
across a dozen little projects gets old fast. `py-modu` gives Python the
same convenience:

```bash
pyrun .
```

That's it. No filename to remember or type.

## Table of contents

- [Why py-modu](#why-py-modu)
- [Installation](#installation)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Comparison with Go](#comparison-with-go)
- [FAQ](#faq)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Why py-modu

Python doesn't have a single, obvious "run the project" command the way Go,
Rust (`cargo run`), or Node (`npm start`) do. `py-modu` is a small, focused
tool that fills that gap for simple scripts and small projects — it doesn't
try to be a build system, a dependency manager, or a task runner. It does
one thing: figure out what you meant by "run this," and run it.

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

On Windows (PowerShell), use `py` instead of `python3`:

```powershell
py -m pip install --user pipx
py -m pipx ensurepath
```

**Important — this step alone won't make `pipx` runnable yet.**
`ensurepath` edits your shell's config file (`~/.zshrc`, `~/.bashrc`, etc.),
but your *currently open* terminal already loaded its environment before
that edit happened, so it won't see the change until you either:

```bash
source ~/.zshrc     # zsh most macOS terminals and many Linux distros
# or
source ~/.bashrc    # bash
```

or just close the terminal and open a new one that's the guaranteed
fix, since a fresh shell reads the config from scratch.

If `pipx` still isn't found after reloading, run this to confirm the
`PATH` edit actually landed in the file you'd expect:

```bash
grep -n "\.local/bin" ~/.zshrc   # or ~/.bashrc
```

If nothing prints, `ensurepath` wrote to a different file than the one
your shell reads on startup (this happens on some setups, e.g. it writes
to `~/.zprofile` instead of `~/.zshrc`). Add the line manually and reload:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Don't want to wait or reload at all?** Call `pipx` through Python
directly this works immediately in the same terminal session, bypassing
the `PATH` issue entirely:

```bash
python3 -m pipx install py-modu
```

Once you've reloaded your shell (or opened a new one) at least once
afterward, the plain `pipx` and `pyrun` commands work normally from then on.

### Alternative: pip

```bash
pip install py-modu
```

#### "externally-managed-environment" error

On Debian/Ubuntu (Ubuntu 23.04+, Debian 12+) and some other distros, a
plain `pip install` outside a virtual environment is blocked by default
(PEP 668) and fails with:

```
error: externally-managed-environment
× This environment is externally managed
```

This is a safety feature protecting your system's Python install, not a
bug in `py-modu`. Pick one:

1. **Use pipx** (see above) the cleanest fix, no flags needed, this is
   exactly the problem pipx exists to solve.
2. **Install into a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # .venv\Scripts\activate on Windows
   pip install py-modu
   ```
   `pyrun` will only be available while that venv is active.
3. **Override the protection directly**, as the error message itself
   suggests works, but only reach for this if 1 and 2 don't fit your
   situation, since it's telling `pip` to bypass your OS's own safety check:
   ```bash
   pip install --user py-modu --break-system-packages
   ```

### Verifying the install

```bash
pyrun --version
```

Should print `pyrun 0.1.1`. If you get a "command not found" error right
after a `pipx install`, it usually means your shell hasn't picked up the
updated `PATH` yet open a new terminal window, or run
`pipx ensurepath` again and restart.

**Compatibility**: Python 3.8 and newer. Tested in CI on Linux, macOS, and
Windows across Python 3.8 through 3.13.

## Usage

### Run the current project

```bash
pyrun .
```

`py-modu` looks for an entry point in the current directory, in this order:

1. `main.py`
2. `app.py`
3. `run.py`
4. If none of those exist but there's exactly **one** `.py` file in the
   directory, that file is used.

If there are multiple `.py` files and none matches the list above,
`py-modu` refuses to guess and tells you what to do instead it will
never silently pick the wrong file.

### Run a specific file

```bash
pyrun path/to/script.py
```

Bypasses auto-detection entirely and just runs that file.

### Pass arguments through to your script

Anything after `--` goes straight into your script's `sys.argv`:

```bash
pyrun . -- --input data.csv --verbose
```

Inside `main.py`, `sys.argv[1:]` would be `['--input', 'data.csv', '--verbose']`,
exactly as if you'd run `python3 main.py --input data.csv --verbose` directly.

### Check the version or see all options

```bash
pyrun --version
pyrun --help
```

## How it works

`py-modu` is intentionally simple under the hood no magic, no config
files, no daemon process.

1. **Discovery**: it lists `.py` files in the target directory and applies
   the `main.py` → `app.py` → `run.py` → single-file rule described above.
2. **Execution**: it runs the chosen file as a real subprocess
   `subprocess.run([sys.executable, target_file, *your_args])` not an
   `import`. This matters for two reasons:
   - `if __name__ == "__main__":` in your script behaves exactly as it
     would if you'd run it directly.
   - Your script's exit code is passed back through as `pyrun`'s own exit
     code, so `pyrun .` works correctly inside CI pipelines and shell
     scripts that check `$?`.
3. **Interpreter resolution**: it uses `sys.executable`, i.e. whichever
   Python interpreter is currently active. Run it inside an activated
   virtualenv and your project's dependencies are available exactly as if
   you'd typed `python3 file.py` yourself `py-modu` doesn't create,
   manage, or need to know about virtual environments at all.

## Comparison with Go

| | Go | py-modu |
|---|---|---|
| Run current project | `go run .` | `pyrun .` |
| Run a specific file | `go run script.go` | `pyrun script.py` |
| Entry point convention | package `main`, func `main()` | `main.py`, `app.py`, or `run.py` |
| Pass arguments | `go run . -- args` | `pyrun . -- args` |
| Ambiguous entry point | compile error | explicit message, asks you to disambiguate |

## FAQ

**Why not just use `python3 script.py`?**
You still can `py-modu` doesn't replace anything or change how Python
itself runs files. It just removes the need to remember or type the exact
filename, the way `go run .` does for Go. It's a small quality-of-life
tool for people who bounce between a lot of small scripts and projects.

**Does it work with virtual environments?**
Yes, activate your venv first, then run `pyrun .` as normal. It uses
whatever interpreter is currently active.

**Does it manage dependencies, like `poetry` or `uv`?**
No. `py-modu` only decides *which file to run* it has no opinion about
package management. Use it alongside `pip`, `poetry`, `uv`, or whatever
you already use.

**What if I have both `main.py` and `app.py`?**
`main.py` wins the check order is fixed and always favors `main.py`
first, matching the Go convention this tool is modeled on.

**Can I use it in a Makefile or CI pipeline?**
Yes. Because `pyrun` runs your script as a real subprocess and forwards
its exit code, `pyrun .` behaves like any other command for the purposes
of `&&`, `set -e`, or a CI step's pass/fail status.

## Troubleshooting

| Problem | Fix |
|---|---|
| `pyrun: command not found` right after `pipx install` | Your shell hasn't reloaded its `PATH` yet see [pipx PATH gotcha](#recommended-pipx-isolated-global-no-system-conflicts), or run `source ~/.zshrc` / `source ~/.bashrc` |
| `zsh: command not found: pipx` right after `ensurepath` | Same cause as above — reload your shell config, or use `python3 -m pipx install py-modu` in the meantime |
| `Error: no Python files found` | You're not in the directory you think you are — check `pwd` |
| `Error: found multiple Python files ... and none is named main.py/app.py/run.py` | Rename your entry file to one of those three, or run it explicitly: `pyrun yourfile.py` |
| Wrong Python version / missing packages when running | Make sure your virtualenv is activated *before* running `pyrun .` |
| `pip install py-modu` fails with "externally-managed-environment" | See [externally-managed-environment error](#externally-managed-environment-error) above |

## Development

```bash
git clone https://github.com/maxchichar/py-modu.git
cd py-modu
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Project layout:

```
py-modu/
├── src/py_modu/
│   ├── __init__.py     # exposes main() and __version__
│   ├── __main__.py     # enables `python -m py_modu`
│   └── core.py         # entry-point discovery + execution logic
├── tests/
│   └── test_core.py
├── pyproject.toml
└── README.md
```

## Contributing

Issues and pull requests are welcome. Before opening a PR:

```bash
pip install -e ".[dev]"
pytest
```

Please keep changes focused `py-modu` is intentionally small in scope.

## License

MIT. see [LICENSE](LICENSE).