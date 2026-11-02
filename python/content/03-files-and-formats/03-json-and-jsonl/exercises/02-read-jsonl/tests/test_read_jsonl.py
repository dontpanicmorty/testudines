from solution import read_events


def test_mixed(tmp_path):
    p = tmp_path / "e.jsonl"
    p.write_text('{"id": 1}\n{"id": 2\n\n[1]\n{"id": 3}\n', encoding="utf-8")
    events, bad = read_events(p)
    assert events == [{"id": 1}, {"id": 3}]
    assert bad == 2


def test_clean(tmp_path):
    p = tmp_path / "e.jsonl"
    p.write_text('{"a": 1}\n{"a": 2}', encoding="utf-8")
    assert read_events(p) == ([{"a": 1}, {"a": 2}], 0)


def test_scalar_line_is_bad(tmp_path):
    p = tmp_path / "e.jsonl"
    p.write_text('42\n"text"\n{"a": 1}\n', encoding="utf-8")
    assert read_events(p) == ([{"a": 1}], 2)
