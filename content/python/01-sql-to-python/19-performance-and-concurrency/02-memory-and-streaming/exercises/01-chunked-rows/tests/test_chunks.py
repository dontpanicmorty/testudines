import inspect

import pytest

from solution import read_in_chunks


@pytest.fixture
def csv_path(tmp_path):
    p = tmp_path / "rows.csv"
    p.write_text("id,name\n" + "".join(f"{i},n{i}\n" for i in range(1, 11)))
    return p


def test_is_generator(csv_path):
    assert inspect.isgenerator(read_in_chunks(csv_path, 3))


def test_chunk_sizes(csv_path):
    assert [len(b) for b in read_in_chunks(csv_path, 4)] == [4, 4, 2]


def test_exact_multiple_has_no_empty_tail(csv_path):
    assert [len(b) for b in read_in_chunks(csv_path, 5)] == [5, 5]


def test_rows_are_dicts_in_order(csv_path):
    first = next(read_in_chunks(csv_path, 3))
    assert first == [{"id": "1", "name": "n1"}, {"id": "2", "name": "n2"}, {"id": "3", "name": "n3"}]


def test_all_rows_preserved(csv_path):
    flat = [r["id"] for b in read_in_chunks(csv_path, 3) for r in b]
    assert flat == [str(i) for i in range(1, 11)]


def test_size_larger_than_file(csv_path):
    assert [len(b) for b in read_in_chunks(csv_path, 100)] == [10]


def test_header_only_yields_nothing(tmp_path):
    p = tmp_path / "e.csv"
    p.write_text("id,name\n")
    assert list(read_in_chunks(p, 3)) == []


def test_invalid_size(csv_path):
    with pytest.raises(ValueError):
        list(read_in_chunks(csv_path, 0))


def test_lazy_does_not_read_ahead(csv_path):
    gen = read_in_chunks(csv_path, 2)
    assert len(next(gen)) == 2    # works without consuming the rest
    gen.close()
