from solution import letter_grade


def test_a():
    assert letter_grade(91) == "A"


def test_boundaries():
    assert letter_grade(80) == "A"
    assert letter_grade(79) == "B"
    assert letter_grade(65) == "B"
    assert letter_grade(64) == "C"
    assert letter_grade(50) == "C"
    assert letter_grade(49) == "F"


def test_extremes():
    assert letter_grade(100) == "A"
    assert letter_grade(0) == "F"
