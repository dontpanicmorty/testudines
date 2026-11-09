from solution import total_dollars


def test_basic():
    assert total_dollars("tea $3.50 and cake $4.25, tip 2.00, gum $1") == 7.75


def test_none():
    assert total_dollars("free") == 0.0


def test_no_dollar_sign_ignored():
    assert total_dollars("12.50") == 0.0


def test_empty():
    assert total_dollars("") == 0.0


def test_floating_error_rounded():
    assert total_dollars("$0.10 $0.20") == 0.3


def test_dot_is_literal():
    assert total_dollars("$3x50") == 0.0
