import os

import pytest

import solution
from solution import sum_of_squares


def test_small():
    assert sum_of_squares([1, 2, 3, 4], workers=2) == 30


def test_matches_builtin_large():
    nums = list(range(50_000))
    assert sum_of_squares(nums, workers=3) == sum(n * n for n in nums)


def test_empty():
    assert sum_of_squares([], workers=4) == 0


def test_fewer_numbers_than_workers():
    assert sum_of_squares([5], workers=4) == 25


def test_single_worker():
    assert sum_of_squares([1, 2, 3], workers=1) == 14


def test_negative_numbers():
    assert sum_of_squares([-3, 3], workers=2) == 18


def test_invalid_workers():
    with pytest.raises(ValueError):
        sum_of_squares([1], workers=0)


def test_uses_process_pool():
    src = open(solution.__file__).read()
    assert "ProcessPoolExecutor" in src, "the prompt asks for a ProcessPoolExecutor"


def test_input_not_mutated():
    nums = [3, 1, 2]
    sum_of_squares(nums, workers=2)
    assert nums == [3, 1, 2]
