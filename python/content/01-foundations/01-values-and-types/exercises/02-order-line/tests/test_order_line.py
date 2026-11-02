from solution import order_line


def test_simple():
    assert order_line("Notebook", 3, 4.5) == "3 x Notebook @ $4.50 = $13.50"


def test_thousands():
    assert order_line("Standing Desk", 2, 600) == "2 x Standing Desk @ $600.00 = $1,200.00"
