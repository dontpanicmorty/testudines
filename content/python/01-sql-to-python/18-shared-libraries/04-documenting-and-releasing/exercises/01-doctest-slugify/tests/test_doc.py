import doctest

import solution
from solution import slugify


def test_doctests_pass_and_enough_examples():
    result = doctest.testmod(solution)
    assert result.failed == 0, f"{result.failed} docstring example(s) fail"
    assert result.attempted >= 5, "add at least one more >>> example of your own"


def test_behaviour():
    assert slugify("Hello,  World!") == "hello-world"
    assert slugify("a_b c") == "a-b-c"
    assert slugify("") == ""
    assert slugify("2026 Plan") == "2026-plan"
