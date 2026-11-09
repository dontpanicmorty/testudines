import warnings
from pathlib import Path

import pytest

from solution import deprecated


@deprecated("new_total")
def old_total(prices, *, scale=1):
    """Add prices."""
    return sum(prices) * scale


def test_warns_with_exact_message():
    with pytest.warns(DeprecationWarning) as record:
        old_total([1, 2])
    assert str(record[0].message) == "old_total is deprecated; use new_total"


def test_return_value_and_arguments_pass_through():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert old_total([1, 2, 3]) == 6
        assert old_total([1, 2, 3], scale=10) == 60


def test_warning_points_at_the_caller():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        old_total([1])
    assert len(caught) == 1
    assert Path(caught[0].filename).resolve() == Path(__file__).resolve(), (
        f"warning is attributed to {caught[0].filename}; use stacklevel=2"
    )


def test_metadata_is_preserved():
    assert old_total.__name__ == "old_total"
    assert old_total.__doc__ == "Add prices."


def test_warns_on_every_call():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        old_total([1])
        old_total([2])
    assert len(caught) == 2


def test_each_decorated_function_uses_its_own_names():
    @deprecated("b")
    def a():
        return 1

    with pytest.warns(DeprecationWarning, match="a is deprecated; use b"):
        assert a() == 1
