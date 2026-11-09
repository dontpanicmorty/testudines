from solution import tally


def test_mixed_case():
    assert tally("Banana band", "b") == 2


def test_missing():
    assert tally("sky", "z") == 0


def test_empty_text():
    assert tally("", "a") == 0


def test_capital_letter_argument():
    assert tally("aAa", "A") == 3
