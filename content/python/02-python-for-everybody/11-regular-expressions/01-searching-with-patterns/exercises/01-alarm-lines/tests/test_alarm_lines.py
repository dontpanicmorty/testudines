from solution import is_alarm


def test_true():
    assert is_alarm("ERROR: disk full") is True


def test_middle_does_not_count():
    assert is_alarm("see ERROR: later") is False


def test_case_matters():
    assert is_alarm("error: disk full") is False


def test_missing_colon():
    assert is_alarm("ERROR disk full") is False


def test_empty_line():
    assert is_alarm("") is False
