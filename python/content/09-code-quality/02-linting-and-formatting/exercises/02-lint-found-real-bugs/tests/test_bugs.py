import subprocess
import sys
from pathlib import Path

from solution import add_tag, make_filters


def test_ruff_bugbear_is_clean():
    r = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "--isolated", "--no-cache", "--select", "B,E,F",
         "--output-format", "concise", "solution.py"],
        capture_output=True, text=True, timeout=60,
    )
    assert r.returncode == 0, "ruff still reports problems:\n" + r.stdout
    assert "noqa" not in Path("solution.py").read_text()


def test_add_tag_calls_are_independent():
    assert add_tag("a") == ["a"]
    assert add_tag("b") == ["b"]


def test_add_tag_extends_given_list():
    mine = ["x"]
    result = add_tag("y", mine)
    assert result == ["x", "y"]
    assert result is mine


def test_each_filter_uses_its_own_threshold():
    low, high = make_filters([10, 50])
    assert low({"value": 20}) is True
    assert high({"value": 20}) is False
    assert high({"value": 50}) is True


def test_three_filters():
    f1, f2, f3 = make_filters([1, 2, 3])
    assert [f({"value": 2}) for f in (f1, f2, f3)] == [True, True, False]


def test_no_thresholds():
    assert make_filters([]) == []
