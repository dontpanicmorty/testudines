import subprocess
import sys
from pathlib import Path

import solution


def test_ruff_is_clean():
    r = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "--isolated", "--no-cache", "--select", "E,F,I,B,UP,SIM",
         "--output-format", "concise", "solution.py"],
        capture_output=True, text=True, timeout=60,
    )
    assert r.returncode == 0, "ruff still reports problems:\n" + r.stdout


def test_no_noqa():
    assert "noqa" not in Path("solution.py").read_text(), "Fix the problems instead of silencing them."


def test_read_config(tmp_path):
    good = tmp_path / "c.json"
    good.write_text('{"a": 1}')
    bad = tmp_path / "bad.json"
    bad.write_text("{nope")
    assert solution.read_config(good) == {"a": 1}
    assert solution.read_config(bad) is None
    assert solution.read_config(tmp_path / "missing.json") is None


def test_has_key():
    assert solution.has_key(None, "a") is False
    assert solution.has_key({"a": None}, "a") is False
    assert solution.has_key({}, "a") is False
    assert solution.has_key({"a": 0}, "a") is True


def test_add_name():
    solution.names.clear()
    solution.add_name("ada")
    solution.add_name("grace")
    assert solution.names == ["ada", "grace"]
