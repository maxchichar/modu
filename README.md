# py-modu 🚀

`py-modu` is a lightweight, Go-inspired command-line utility for Python developers. It brings the simplicity of Go's workflow to Python by providing a global binary command that executes your code directories instantly.

Instead of typing exact filenames like `python3 very_long_filename_test.py`, you simply type `py run .`.

---

## Features

- **Zero Configuration**: No hardcoded main file requirements.
- **Smart Detection**: Automatically scans your working directory for any `.py` file.
- **Timestamp Priority**: If multiple Python files exist, it automatically executes the most recently modified one.

---

## Installation

### Standard Global Installation
To use `py` anywhere across your machine without restrictions, run:

```bash
python3 -m pip install py-modu --break-system-packages
```
*(Note: Re-open your terminal or run `rehash` if the command is not picked up instantly).*

### System Path Configuration (Linux/macOS troubleshooting)
If your terminal returns `zsh: command not found: py` after installation, Python's user binary path is missing from your environment. Add it by running:

```bash
echo 'export PATH="HOME/.local/bin:PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## Usage

Navigate to any directory containing Python files and run:

```bash
py run .
```

### Working inside Virtual Environments (`venv`)
If you install `py-modu` inside a local project virtual environment, the global shell hook is scoped inside that space. You must activate the environment first:

```bash
# 1. Activate your local environment
source .venv/bin/activate

# 2. Run the shortcut cleanly
py run .
```
Alternatively, call the environment binary directly without activation:
```bash
./.venv/bin/py run .
```

---

## How It Works Under the Hood

When you execute `py run .`:
1. It validates the positional arguments.
2. It fetches all `.py` files inside your current active folder directory.
3. It sorts them using file modification metadata (`os.path.getmtime`).
4. It calls your active system Python interpreter to spin up a process running your code.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
