import re
import subprocess
import sys
from pathlib import Path

from solution import average_age, find_email, total_rows


def test_mypy_strict_passes():
    r = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "--no-incremental", "--cache-dir", ".mypy_cache_dojo",
         "solution.py", "check_usage.py"],
        capture_output=True, text=True, timeout=90,
    )
    assert r.returncode == 0, "mypy --strict reported problems:\n" + r.stdout


def test_no_escape_hatches():
    src = Path("solution.py").read_text()
    assert "type: ignore" not in src, "Fix the types instead of silencing mypy."
    assert "cast(" not in src and not re.search(r"\bAny\b", src), "Don't use cast or Any."


def test_find_email():
    assert find_email("c1") == "ada@example.com"
    assert find_email("zzz") is None


def test_average_age():
    assert average_age([20, 25]) == 22.5
    assert average_age([20, 30, 40]) == 30.0


def test_total_rows():
    assert total_rows([1, 2, 3]) == 6
    assert total_rows([]) == 0
