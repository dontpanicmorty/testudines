import csv

import pytest

from solution import write_chunks


def read(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def test_splits_and_names(tmp_path):
    rows = ({"id": i, "name": f"n{i}"} for i in range(5))
    paths = write_chunks(rows, tmp_path, "orders", 2, ["id", "name"])
    assert [p.name for p in paths] == ["orders_0001.csv", "orders_0002.csv", "orders_0003.csv"]
    assert [len(read(p)) for p in paths] == [2, 2, 1]
    assert [r["id"] for p in paths for r in read(p)] == ["0", "1", "2", "3", "4"]


def test_header_in_every_file(tmp_path):
    paths = write_chunks([{"a": 1}, {"a": 2}], tmp_path, "x", 1, ["a"])
    for p in paths:
        assert p.read_text().splitlines()[0] == "a"


def test_exact_multiple_has_no_empty_trailing_file(tmp_path):
    paths = write_chunks([{"a": i} for i in range(4)], tmp_path, "x", 2, ["a"])
    assert len(paths) == 2
    assert sorted(p.name for p in tmp_path.iterdir()) == ["x_0001.csv", "x_0002.csv"]


def test_no_rows_no_files(tmp_path):
    assert write_chunks([], tmp_path, "x", 3, ["a"]) == []
    assert list(tmp_path.iterdir()) == []


def test_streams_lazily(tmp_path):
    consumed = []

    def gen():
        for i in range(6):
            consumed.append(i)
            yield {"a": i}

    paths = write_chunks(gen(), tmp_path, "x", 3, ["a"])
    assert len(paths) == 2 and consumed == list(range(6))


def test_bad_max_rows(tmp_path):
    with pytest.raises(ValueError):
        write_chunks([{"a": 1}], tmp_path, "x", 0, ["a"])
