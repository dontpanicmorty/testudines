import pytest

from solution import HttpError, is_transient


@pytest.mark.parametrize("exc", [
    TimeoutError(), ConnectionError(), ConnectionResetError(),
    HttpError(429), HttpError(500), HttpError(503),
])
def test_transient(exc):
    assert is_transient(exc) is True, repr(exc)


@pytest.mark.parametrize("exc", [
    ValueError("bad"), KeyError("k"), HttpError(400), HttpError(401),
    HttpError(404), HttpError(499),
])
def test_permanent(exc):
    assert is_transient(exc) is False, repr(exc)
