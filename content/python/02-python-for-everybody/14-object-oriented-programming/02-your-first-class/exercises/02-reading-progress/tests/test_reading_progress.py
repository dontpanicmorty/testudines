from solution import Book


def test_str_and_percent():
    b = Book("Tide Tables", 200)
    b.read(30)
    assert str(b) == "Tide Tables (30/200)"
    assert b.percent() == 15
    assert b.pages_left() == 170


def test_cannot_pass_the_end():
    b = Book("Short", 10)
    b.read(8)
    b.read(8)
    assert b.pages_left() == 0
    assert str(b) == "Short (10/10)"
    assert b.percent() == 100


def test_fresh_book():
    b = Book("New", 3)
    assert b.percent() == 0
    assert str(b) == "New (0/3)"


def test_rounding():
    b = Book("Thirds", 3)
    b.read(1)
    assert b.percent() == 33
    b.read(1)
    assert b.percent() == 67
