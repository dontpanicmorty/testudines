import pytest

from solution import ValidationError, validate_customer


def test_clean():
    out = validate_customer({"customer_id": "5", "email": " A@B.com ", "plan": "PRO"})
    assert out == {"customer_id": 5, "email": "a@b.com", "plan": "pro"}


def test_all_errors_reported():
    with pytest.raises(ValidationError) as exc:
        validate_customer({"customer_id": "abc", "email": "nope", "plan": "gold"})
    msg = str(exc.value)
    assert "customer_id" in msg and "email" in msg and "plan" in msg
    assert msg.count(";") == 2, f"expected three problems joined by '; ', got {msg!r}"


def test_non_positive_id():
    with pytest.raises(ValidationError):
        validate_customer({"customer_id": "0", "email": "a@b.c", "plan": "free"})


def test_two_ats():
    with pytest.raises(ValidationError):
        validate_customer({"customer_id": "1", "email": "a@b@c", "plan": "free"})


def test_is_value_error():
    assert issubclass(ValidationError, ValueError)


def test_missing_keys():
    with pytest.raises(ValidationError):
        validate_customer({})
