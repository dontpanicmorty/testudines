from datetime import date
import pytest
from pydantic import ValidationError
from solution import Customer


def test_normalised():
    c = Customer(customer_id="7", email="  Ada@Example.COM ", signup_date="2024-06-12")
    assert c.email == "ada@example.com", f"got {c.email!r}"
    assert c.customer_id == 7 and c.signup_date == date(2024, 6, 12)


@pytest.mark.parametrize("bad", ["nope", "  ", ""])
def test_bad_email_rejected(bad):
    with pytest.raises(ValidationError):
        Customer(customer_id=1, email=bad, signup_date="2024-06-12")


def test_error_mentions_email_field():
    with pytest.raises(ValidationError) as e:
        Customer(customer_id=1, email="nope", signup_date="2024-06-12")
    assert e.value.errors()[0]["loc"] == ("email",)
