import warnings

from datakit import deprecated


@deprecated("new_add", removed_in="2.0.0")
def old_add(a, b=0):
    """Add two numbers."""
    return a + b


@deprecated("other")
def plain():
    return "x"


def test_result_passthrough():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert old_add(1, b=2) == 3
        assert old_add(5) == 5


def test_warns_with_details_and_caller_location():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        old_add(1, 2)
    assert len(caught) == 1
    w = caught[0]
    assert issubclass(w.category, DeprecationWarning)
    text = str(w.message)
    assert "old_add" in text and "new_add" in text and "2.0.0" in text
    assert w.filename == __file__, f"warning points at {w.filename}, use stacklevel=2"


def test_warns_every_call():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        plain()
        plain()
    assert len(caught) == 2
    assert "removed in" not in str(caught[0].message)


def test_metadata_preserved():
    assert old_add.__name__ == "old_add"
    assert old_add.__doc__ == "Add two numbers."
