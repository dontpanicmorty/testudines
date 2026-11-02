import pytest

from datakit import RowValidator


def make():
    return RowValidator(
        required=["order_id", "status"],
        types={"order_id": int, "amount": float},
        checks={"amount": lambda v: v >= 0, "status": lambda v: v in {"open", "closed"}},
    )


def test_valid_row_has_no_errors():
    assert make().errors({"order_id": 1, "status": "open", "amount": 2.5}) == []


def test_required_missing_none_and_blank():
    v = make()
    assert v.errors({"status": "open"}) == ["order_id: required"]
    assert v.errors({"order_id": None, "status": "open"}) == ["order_id: required"]
    assert v.errors({"order_id": 1, "status": "  "}) == ["status: required"]


def test_wrong_type():
    assert make().errors({"order_id": "1", "status": "open"}) == ["order_id: expected int"]


def test_bool_is_not_an_int():
    assert make().errors({"order_id": True, "status": "open"}) == ["order_id: expected int"]


def test_failed_check():
    assert make().errors({"order_id": 1, "status": "open", "amount": -1.0}) == ["amount: failed check"]
    assert make().errors({"order_id": 1, "status": "weird"}) == ["status: failed check"]


def test_check_that_raises_counts_as_failure_not_crash():
    v = RowValidator(checks={"x": lambda value: value > 0})
    assert v.errors({"x": "text"}) == ["x: failed check"]


def test_absent_optional_fields_are_skipped():
    assert make().errors({"order_id": 1, "status": "open"}) == []


def test_multiple_errors_are_all_reported():
    errs = make().errors({"order_id": "x", "status": "weird", "amount": "free"})
    assert errs == ["order_id: expected int", "amount: expected float", "status: failed check"]


def test_check_skipped_when_type_is_wrong():
    # amount is a str so only the type error is reported, not a confusing failed check
    errs = make().errors({"order_id": 1, "status": "open", "amount": "-5"})
    assert errs == ["amount: expected float"]


def test_split():
    rows = [
        {"order_id": 1, "status": "open"},
        {"order_id": "bad", "status": "open"},
        {"order_id": 3, "status": "closed"},
    ]
    valid, invalid = make().split(rows)
    assert [r["order_id"] for r in valid] == [1, 3]
    assert invalid == [({"order_id": "bad", "status": "open"}, ["order_id: expected int"])]


def test_split_accepts_generators_and_returns_copies():
    rows = ({"order_id": i, "status": "open"} for i in range(3))
    valid, invalid = make().split(rows)
    assert len(valid) == 3 and invalid == []
    original = {"order_id": 1, "status": "open"}
    out, _ = make().split([original])
    out[0]["order_id"] = 99
    assert original["order_id"] == 1


def test_validator_with_no_rules_accepts_everything():
    assert RowValidator().errors({"anything": object()}) == []


def test_keyword_only_constructor():
    with pytest.raises(TypeError):
        RowValidator(["a"])
