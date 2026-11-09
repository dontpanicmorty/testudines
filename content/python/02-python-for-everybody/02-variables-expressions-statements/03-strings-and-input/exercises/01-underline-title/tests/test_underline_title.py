from solution import with_underline


def test_short():
    assert with_underline("Menu") == "Menu\n----"


def test_with_space():
    assert with_underline("Hot tea") == "Hot tea\n-------"


def test_one_letter():
    assert with_underline("A") == "A\n-"


def test_empty():
    assert with_underline("") == "\n"
