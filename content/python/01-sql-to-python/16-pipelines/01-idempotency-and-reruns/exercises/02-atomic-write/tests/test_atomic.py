import pytest

from solution import atomic_write


def test_creates_file(tmp_path):
    target = tmp_path / "daily.csv"
    atomic_write(target, lambda fh: fh.write("a,b\n1,2\n"))
    assert target.read_text() == "a,b\n1,2\n"


def test_replaces_existing(tmp_path):
    target = tmp_path / "daily.csv"
    target.write_text("old")
    atomic_write(target, lambda fh: fh.write("new"))
    assert target.read_text() == "new"
    assert [p.name for p in tmp_path.iterdir()] == ["daily.csv"], "temp file left behind"


def test_failure_keeps_original_and_cleans_up(tmp_path):
    target = tmp_path / "daily.csv"
    target.write_text("original")

    def produce(fh):
        fh.write("partial")
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        atomic_write(target, produce)
    assert target.read_text() == "original"
    assert [p.name for p in tmp_path.iterdir()] == ["daily.csv"], "temp file left behind"


def test_failure_when_target_missing(tmp_path):
    target = tmp_path / "new.csv"
    with pytest.raises(ValueError):
        atomic_write(target, lambda fh: (_ for _ in ()).throw(ValueError("x")))
    assert list(tmp_path.iterdir()) == []
