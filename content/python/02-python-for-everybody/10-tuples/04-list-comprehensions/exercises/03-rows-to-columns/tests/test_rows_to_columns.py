import pytest

from solution import columns_of


def test_basic():
    assert columns_of([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]


def test_empty():
    assert columns_of([]) == []


def test_single_row():
    assert columns_of([["a", "b"]]) == [["a"], ["b"]]


def test_ragged_raises():
    with pytest.raises(ValueError):
        columns_of([[1, 2], [3]])


def test_input_unchanged():
    rows = [[1, 2], [3, 4]]
    columns_of(rows)
    assert rows == [[1, 2], [3, 4]]


def test_rows_of_zero_length():
    assert columns_of([[], []]) == []
