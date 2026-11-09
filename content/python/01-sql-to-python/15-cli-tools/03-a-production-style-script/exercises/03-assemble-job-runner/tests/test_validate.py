import pytest

from jobrunner.validate import validate_row

GOOD = {"order_id": "7", "amount": "19.50", "status": "Shipped "}


def test_valid_row():
    assert validate_row(GOOD) == []


@pytest.mark.parametrize("field,value", [
    ("order_id", "x"), ("order_id", "0"), ("order_id", "-3"), ("order_id", ""),
    ("amount", "abc"), ("amount", "-0.01"), ("amount", ""),
    ("status", "lost"), ("status", ""),
])
def test_each_bad_field_reported_with_its_name(field, value):
    problems = validate_row({**GOOD, field: value})
    assert len(problems) == 1, problems
    assert problems[0].startswith(field + ":")


def test_multiple_problems_and_missing_keys():
    problems = validate_row({})
    assert sorted(p.split(":")[0] for p in problems) == ["amount", "order_id", "status"]
