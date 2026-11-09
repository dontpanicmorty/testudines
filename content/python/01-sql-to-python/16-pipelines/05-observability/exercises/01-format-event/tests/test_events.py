import json

from solution import format_event, parse_events


def test_format_sorted_single_line():
    s = format_event("load_finished", table="orders", rows=500)
    assert s == '{"event": "load_finished", "rows": 500, "table": "orders"}'
    assert "\n" not in s


def test_format_no_fields():
    assert json.loads(format_event("start")) == {"event": "start"}


def test_parse_skips_garbage():
    text = '{"event": "a"}\nnot json\n\n   \n{"event": "b", "n": 1}\n'
    assert parse_events(text) == [{"event": "a"}, {"event": "b", "n": 1}]


def test_parse_ignores_non_objects():
    assert parse_events('[1, 2]\n"text"\n42\n{"event": "x"}') == [{"event": "x"}]


def test_roundtrip():
    s = format_event("x", a=1, b="two")
    assert parse_events(s) == [{"event": "x", "a": 1, "b": "two"}]
