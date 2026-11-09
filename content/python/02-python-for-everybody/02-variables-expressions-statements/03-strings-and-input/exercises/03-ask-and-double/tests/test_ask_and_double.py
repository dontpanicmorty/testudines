from solution import double_my_number


def run_with(monkeypatch, typed):
    monkeypatch.setattr("builtins.input", lambda *args: typed)
    return double_my_number()


def test_whole(monkeypatch):
    assert run_with(monkeypatch, "21") == 42


def test_decimal(monkeypatch):
    assert run_with(monkeypatch, "1.5") == 3.0


def test_negative(monkeypatch):
    assert run_with(monkeypatch, "-4") == -8


def test_zero(monkeypatch):
    assert run_with(monkeypatch, "0") == 0
