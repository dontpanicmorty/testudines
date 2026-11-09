from solution import Session


def test_open_on_create():
    log = []
    s = Session(log, "alpha")
    assert log == ["open alpha"]
    assert s.name == "alpha"


def test_close_on_delete():
    log = []
    s = Session(log, "alpha")
    del s
    assert log == ["open alpha", "close alpha"]


def test_two_sessions_in_order():
    log = []
    a = Session(log, "a")
    b = Session(log, "b")
    del a
    del b
    assert log == ["open a", "open b", "close a", "close b"]


def test_reassigning_discards_old():
    log = []
    s = Session(log, "first")
    s = Session(log, "second")
    assert log == ["open first", "open second", "close first"]
