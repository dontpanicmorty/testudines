from contract import check_contract
from library import parse_amount


def test_passing_contract():
    cases = [
        (("$1,234.50",), {}, 1234.5),
        (("  7 ",), {}, 7.0),
        (("EUR 9",), {"currency": "EUR "}, 9.0),
        (("abc",), {}, ValueError),
    ]
    assert check_contract(parse_amount, cases) == []


def test_wrong_value():
    out = check_contract(parse_amount, [(("5",), {}, 6.0)])
    assert out == ["case 0: expected 6.0, got 5.0"]


def test_unexpected_exception():
    out = check_contract(parse_amount, [(("5",), {}, 5.0), (("oops",), {}, 1.0)])
    assert out == ["case 1: raised ValueError"]


def test_expected_exception_not_raised():
    out = check_contract(parse_amount, [(("5",), {}, ValueError)])
    assert out == ["case 0: expected ValueError to be raised"]


def test_wrong_exception_type():
    def f():
        raise KeyError("k")
    assert check_contract(f, [((), {}, ValueError)]) == ["case 0: raised KeyError"]


def test_uses_arbitrary_callable_and_keeps_going():
    def f(x, *, y=0):
        return x + y
    cases = [((1,), {"y": 1}, 2), ((1,), {}, 5), ((2,), {}, 2)]
    assert check_contract(f, cases) == ["case 1: expected 5, got 1"]
