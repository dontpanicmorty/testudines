import dataclasses

import pytest

from solution import Pipeline, RunResult


def test_happy_path():
    seen = []

    def load(rows):
        seen.append(rows)
        return len(rows)

    p = Pipeline(lambda: [{"n": "1"}, {"n": "2"}], lambda r: {"n": int(r["n"])}, load)
    assert p.run() == RunResult(2, 2, 0)
    assert seen == [[{"n": 1}, {"n": 2}]]


def test_none_and_value_error_are_rejections():
    def transform(row):
        if row["n"] == "skip":
            return None
        return {"n": int(row["n"])}

    p = Pipeline(lambda: iter([{"n": "1"}, {"n": "skip"}, {"n": "x"}, {"n": "4"}]), transform, len)
    r = p.run()
    assert (r.rows_in, r.rows_out, r.rejected) == (4, 2, 2)


def test_rows_out_is_what_load_returned():
    p = Pipeline(lambda: [{"a": 1}], lambda r: r, lambda rows: 99)
    assert p.run().rows_out == 99


def test_load_called_once_even_when_empty():
    calls = []
    p = Pipeline(lambda: [], lambda r: r, lambda rows: calls.append(rows) or 0)
    assert p.run() == RunResult(0, 0, 0)
    assert calls == [[]]


def test_other_exceptions_propagate():
    def bad(row):
        raise KeyError("boom")

    with pytest.raises(KeyError):
        Pipeline(lambda: [{"a": 1}], bad, len).run()


def test_run_result_is_frozen_dataclass():
    assert dataclasses.is_dataclass(RunResult)
    with pytest.raises(dataclasses.FrozenInstanceError):
        RunResult(1, 1, 0).rows_in = 5


def test_pipeline_is_reusable():
    p = Pipeline(lambda: [{"n": 1}], lambda r: r, len)
    assert p.run() == p.run()
