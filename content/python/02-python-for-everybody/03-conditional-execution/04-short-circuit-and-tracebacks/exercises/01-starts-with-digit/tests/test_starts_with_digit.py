from solution import starts_with_digit


def test_digit_first():
    assert starts_with_digit("7up") is True


def test_letter_first():
    assert starts_with_digit("up7") is False


def test_empty():
    assert starts_with_digit("") is False


def test_only_digit():
    assert starts_with_digit("5") is True
