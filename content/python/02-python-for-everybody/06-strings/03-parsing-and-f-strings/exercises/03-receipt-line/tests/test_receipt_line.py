from solution import receipt_line


def test_basic():
    assert receipt_line("tea", 3, 1.5) == "tea        x3     4.50"


def test_long_name_not_cut():
    assert receipt_line("chocolate-bar", 1, 2) == "chocolate-bar x1     2.00"


def test_rounding():
    assert receipt_line("pen", 3, 0.3333) == "pen        x3     1.00"


def test_bigger_total():
    assert receipt_line("lamp", 2, 1234.5) == "lamp       x2  2469.00"
