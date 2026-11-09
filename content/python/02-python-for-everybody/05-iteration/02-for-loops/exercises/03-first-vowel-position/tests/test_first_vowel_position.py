from solution import first_vowel_index


def test_middle():
    assert first_vowel_index("rhythm and blues") == 7


def test_capital_first():
    assert first_vowel_index("Echo") == 0


def test_none():
    assert first_vowel_index("rhythm") == -1


def test_empty():
    assert first_vowel_index("") == -1
