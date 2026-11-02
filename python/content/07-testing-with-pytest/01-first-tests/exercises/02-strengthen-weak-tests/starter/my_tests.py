from status import normalize_status


def test_active():
    assert normalize_status("active")


def test_returns_string():
    assert isinstance(normalize_status("Paused"), str)


def test_none_does_not_crash():
    normalize_status(None)


def test_junk():
    result = normalize_status("whatever")
    assert result is not None
