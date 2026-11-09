import itertools
from solution import dedupe


def test_basic():
    rows = [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}, {"id": 1, "v": "c"}]
    assert list(dedupe(rows, key=lambda r: r["id"])) == [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}]


def test_composite_key():
    rows = [("a", 1), ("a", 2), ("a", 1)]
    assert list(dedupe(rows, key=lambda r: r)) == [("a", 1), ("a", 2)]


def test_empty():
    assert list(dedupe([], key=lambda r: r)) == []


def test_lazy_on_infinite_stream():
    stream = ({"id": n % 3, "n": n} for n in itertools.count())
    out = list(itertools.islice(dedupe(stream, key=lambda r: r["id"]), 3))
    assert [r["id"] for r in out] == [0, 1, 2]
