from solution import is_reserved


def test_reserved():
    assert is_reserved("while") is True
    assert is_reserved("return") is True


def test_not_reserved():
    assert is_reserved("basket") is False


def test_capital_letters_matter():
    assert is_reserved("True") is True
    assert is_reserved("true") is False


def test_empty():
    assert is_reserved("") is False
