from solution import make_greeting


def test_basic():
    assert make_greeting("Priya") == "Good morning, Priya!"


def test_another_name():
    assert make_greeting("Tomas") == "Good morning, Tomas!"


def test_empty_name():
    assert make_greeting("") == "Good morning, !"
