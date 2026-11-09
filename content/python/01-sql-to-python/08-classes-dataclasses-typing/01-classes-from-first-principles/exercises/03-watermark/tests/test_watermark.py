from solution import Watermark


def test_starts_empty():
    assert Watermark().value is None


def test_start_value():
    assert Watermark("2025-01-01").value == "2025-01-01"


def test_advance_moves_forward():
    w = Watermark()
    assert w.advance("2025-01-05") is True
    assert w.value == "2025-01-05"
    assert w.advance("2025-02-01") is True
    assert w.value == "2025-02-01"


def test_advance_ignores_older_and_equal():
    w = Watermark("2025-01-05")
    assert w.advance("2025-01-03") is False
    assert w.advance("2025-01-05") is False
    assert w.value == "2025-01-05"


def test_is_new():
    w = Watermark()
    assert w.is_new("2000-01-01") is True
    w.advance("2025-01-05")
    assert w.is_new("2025-01-06") is True
    assert w.is_new("2025-01-05") is False
    assert w.is_new("2025-01-04") is False


def test_is_new_does_not_move_it():
    w = Watermark("2025-01-05")
    w.is_new("2030-01-01")
    assert w.value == "2025-01-05"


def test_repr():
    assert repr(Watermark("2025-01-05")) == "Watermark('2025-01-05')"
    assert repr(Watermark()) == "Watermark(None)"
