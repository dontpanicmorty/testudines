import json

import pytest

from solution import TooManyRejects, load_rows


def parse(raw):
    return {"id": int(raw["id"]), "amount": float(raw["amount"])}


def test_good_rows_and_empty_reject_file(tmp_path):
    rp = tmp_path / "rej.jsonl"
    out = load_rows([{"id": "1", "amount": "2.5"}], parse, rp)
    assert out == [{"id": 1, "amount": 2.5}]
    assert rp.exists() and rp.read_text() == ""


def test_rejects_written_with_reason(tmp_path):
    rp = tmp_path / "out" / "rej.jsonl"
    rows = [{"id": str(i), "amount": "1"} for i in range(9)] + [{"id": "x", "amount": "1"}]
    out = load_rows(rows, parse, rp, max_reject_rate=0.2)
    assert len(out) == 9
    lines = [json.loads(l) for l in rp.read_text().splitlines()]
    assert len(lines) == 1
    assert lines[0]["row"] == {"id": "x", "amount": "1"}
    assert "invalid literal" in lines[0]["error"]


def test_threshold_is_strictly_greater(tmp_path):
    rows = [{"id": "1", "amount": "1"}, {"id": "bad", "amount": "1"}]
    out = load_rows(rows, parse, tmp_path / "r.jsonl", max_reject_rate=0.5)
    assert len(out) == 1


def test_too_many_rejects_still_writes_file(tmp_path):
    rp = tmp_path / "r.jsonl"
    rows = [{"id": "a", "amount": "1"}, {"id": "b", "amount": "1"}, {"id": "3", "amount": "1"}]
    with pytest.raises(TooManyRejects):
        load_rows(rows, parse, rp, max_reject_rate=0.2)
    assert len(rp.read_text().splitlines()) == 2


def test_other_errors_propagate(tmp_path):
    with pytest.raises(KeyError):
        load_rows([{"id": "1"}], parse, tmp_path / "r.jsonl")


def test_empty_input(tmp_path):
    assert load_rows([], parse, tmp_path / "r.jsonl") == []
