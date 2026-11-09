from solution import hosts


def test_basic():
    assert hosts("write ana@example.org, or ben@mail.example.com") == ["example.org", "mail.example.com"]


def test_none():
    assert hosts("no addresses") == []


def test_trailing_full_stop():
    assert hosts("contact cy@example.org.") == ["example.org"]


def test_multiple_in_a_row():
    assert hosts("a@x.org b@y.org") == ["x.org", "y.org"]


def test_empty():
    assert hosts("") == []
