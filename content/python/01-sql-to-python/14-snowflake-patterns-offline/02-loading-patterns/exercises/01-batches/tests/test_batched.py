import itertools

import pytest

from solution import batched


def test_exact_and_ragged():
    assert list(batched(range(6), 3)) == [[0, 1, 2], [3, 4, 5]]
    assert list(batched(range(7), 3)) == [[0, 1, 2], [3, 4, 5], [6]]


def test_empty_and_size_larger():
    assert list(batched([], 3)) == []
    assert list(batched([1, 2], 10)) == [[1, 2]]


def test_batches_are_lists():
    assert all(isinstance(b, list) for b in batched("abcde", 2))


def test_lazy_on_infinite_stream():
    gen = batched(itertools.count(), 4)
    assert next(gen) == [0, 1, 2, 3]
    assert next(gen) == [4, 5, 6, 7]


def test_bad_size():
    with pytest.raises(ValueError):
        list(batched([1], 0))
