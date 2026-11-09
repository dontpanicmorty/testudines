import subprocess
import sys
from pathlib import Path

from solution import first_or_none, group_by_region, total_cents


def test_mypy_strict_passes():
    r = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "--no-incremental", "--cache-dir", ".mypy_cache_dojo",
         "solution.py", "check_usage.py"],
        capture_output=True, text=True, timeout=90,
    )
    assert r.returncode == 0, "mypy --strict reported problems:\n" + r.stdout


def test_no_escape_hatches():
    src = Path("solution.py").read_text()
    assert "type: ignore" not in src and "Any" not in src, "Fix the types instead of silencing mypy."


def test_behaviour_unchanged():
    assert total_cents([1.10, 2.20]) == 330
    assert total_cents([]) == 0
    assert first_or_none(["a", "b"]) == "a"
    assert first_or_none([]) is None
    rows = [
        {"region": "EU", "customer_id": "1"},
        {"region": "US", "customer_id": "2"},
        {"region": "EU", "customer_id": "3"},
    ]
    assert group_by_region(rows) == {"EU": ["1", "3"], "US": ["2"]}
