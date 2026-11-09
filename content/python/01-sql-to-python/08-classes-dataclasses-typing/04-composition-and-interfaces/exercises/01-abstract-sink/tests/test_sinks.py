import csv

import pytest

from solution import CsvSink, MemorySink, Sink


def test_sink_is_abstract():
    with pytest.raises(TypeError):
        Sink()


def test_incomplete_subclass_cannot_be_created():
    class Half(Sink):
        pass

    with pytest.raises(TypeError):
        Half()


def test_memory_sink():
    s = MemorySink()
    assert s.write([{"id": 1}, {"id": 2}]) == 2
    assert s.write([{"id": 3}]) == 1
    assert s.rows == [{"id": 1}, {"id": 2}, {"id": 3}]
    assert isinstance(s, Sink)


def test_csv_sink_writes_header_and_rows(tmp_path):
    path = tmp_path / "out.csv"
    assert CsvSink(path).write([{"id": 1, "name": "Ada"}, {"id": 2, "name": "Grace"}]) == 2
    with open(path, newline="") as f:
        assert list(csv.DictReader(f)) == [{"id": "1", "name": "Ada"}, {"id": "2", "name": "Grace"}]


def test_csv_sink_rewrites_file(tmp_path):
    path = tmp_path / "out.csv"
    sink = CsvSink(path)
    sink.write([{"id": 1}, {"id": 2}])
    sink.write([{"id": 9}])
    assert path.read_text().split() == ["id", "9"]


def test_csv_sink_empty_writes_nothing(tmp_path):
    path = tmp_path / "out.csv"
    assert CsvSink(path).write([]) == 0
    assert not path.exists()
