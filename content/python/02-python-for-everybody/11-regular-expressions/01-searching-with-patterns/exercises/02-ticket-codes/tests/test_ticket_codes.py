from solution import is_ticket


def test_valid():
    assert is_ticket("AB-7") is True
    assert is_ticket("QX-20481") is True


def test_lowercase_rejected():
    assert is_ticket("ab-7") is False


def test_no_digits():
    assert is_ticket("AB-") is False


def test_extra_characters_rejected():
    assert is_ticket("xAB-7") is False
    assert is_ticket("AB-7x") is False
    assert is_ticket("AB-7 ") is False


def test_wrong_letter_count():
    assert is_ticket("A-7") is False
    assert is_ticket("ABC-7") is False
