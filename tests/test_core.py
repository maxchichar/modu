import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest

from py_modu.core import _discover_entry


def test_prefers_main_py(tmp_path):
    (tmp_path / "main.py").write_text("print('main')")
    (tmp_path / "helper.py").write_text("print('helper')")
    assert _discover_entry(tmp_path).name == "main.py"


def test_single_file_fallback(tmp_path):
    (tmp_path / "only_script.py").write_text("print('hi')")
    assert _discover_entry(tmp_path).name == "only_script.py"


def test_ambiguous_multiple_files_exits(tmp_path):
    (tmp_path / "a.py").write_text("print('a')")
    (tmp_path / "b.py").write_text("print('b')")
    with pytest.raises(SystemExit):
        _discover_entry(tmp_path)


def test_no_files_exits(tmp_path):
    with pytest.raises(SystemExit):
        _discover_entry(tmp_path)
