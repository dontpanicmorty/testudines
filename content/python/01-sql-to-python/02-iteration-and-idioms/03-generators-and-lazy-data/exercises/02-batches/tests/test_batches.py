import itertools
import pytest
from solution import batches


def test_basic():
    assert list(batches(range(7), 3)) == [[0, 1, 2], [3, 4, 5], [6]]


def test_exact_and_empty():
    assert list(batches([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]
    assert list(batches([], 3)) == []


def test_generator_input():
    assert list(batches((x for x in "abcde"), 2)) == [["a", "b"], ["c", "d"], ["e"]]


def test_infinite_stream_is_lazy():
    gen = batches(itertools.count(), 3)
    assert next(gen) == [0, 1, 2]
    assert next(gen) == [3, 4, 5]


def test_bad_size():
    with pytest.raises(ValueError):
        list(batches([1], 0))
