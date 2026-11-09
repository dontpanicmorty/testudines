from solution import describe_number


def test_negative():
    assert describe_number(-4) == "negative"


def test_zero():
    assert describe_number(0) == "zero"


def test_positive():
    assert describe_number(12) == "positive"


def test_tiny_decimals():
    assert describe_number(-0.001) == "negative"
    assert describe_number(0.001) == "positive"
