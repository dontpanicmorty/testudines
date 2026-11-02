import re
import subprocess
import sys
from pathlib import Path

from solution import ListSink, Sink, route


def ev(uid, value):
    return {"user_id": uid, "name": "click", "value": value}


class RecordingSink:
    def __init__(self):
        self.calls = []

    def write(self, events):
        self.calls.append(list(events))
        return 100 + len(events)


def test_mypy_strict_passes():
    r = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "--no-incremental", "--cache-dir", ".mypy_cache_dojo",
         "solution.py", "check_usage.py"],
        capture_output=True, text=True, timeout=90,
    )
    assert r.returncode == 0, "mypy --strict reported problems:\n" + r.stdout


def test_no_escape_hatches():
    src = Path("solution.py").read_text()
    assert "type: ignore" not in src and "cast(" not in src and not re.search(r"\bAny\b", src)


def test_list_sink():
    s = ListSink()
    assert s.write([ev(1, 1.0), ev(2, 2.0)]) == 2
    assert s.write([ev(3, 3.0)]) == 1
    assert [e["user_id"] for e in s.events] == [1, 2, 3]


def test_list_sink_is_structural_not_inherited():
    assert Sink not in ListSink.__mro__


def test_route_filters_in_one_call_and_returns_write_result():
    rec = RecordingSink()
    events = [ev(1, 0.5), ev(2, 3.0), ev(3, 1.0), ev(4, 2.0)]
    assert route(events, rec, min_value=1.0) == 103
    assert len(rec.calls) == 1
    assert [e["user_id"] for e in rec.calls[0]] == [2, 3, 4]


def test_route_default_threshold_keeps_non_negative_values():
    rec = RecordingSink()
    route([ev(1, 0.0), ev(2, -1.0)], rec)
    assert [e["user_id"] for e in rec.calls[0]] == [1]


def test_route_with_nothing_qualifying_skips_write():
    rec = RecordingSink()
    assert route([ev(1, 0.1)], rec, min_value=5.0) == 0
    assert rec.calls == []
