from solution import row_total


def test_basic():
    assert row_total("4,10,6") == 20


def test_spaces():
    assert row_total(" 4, 10 ") == 14


def test_empty():
    assert row_total("") == 0
    assert row_total("   ") == 0


def test_negative_numbers():
    assert row_total("5,-8") == -3
