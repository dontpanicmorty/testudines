import pandas as pd
from solution import paid_totals


def frame():
    return pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5],
        "customer_id": [10, 10, 20, 30, 40],
        "status": ["paid", "paid", "refunded", "paid", "paid"],
        "amount": [50.0, 25.5, 80.0, 75.5, 1.0],
    })


def test_values_and_order():
    out = paid_totals(frame())
    assert list(out.columns) == ["customer_id", "total"]
    assert out.to_dict("records") == [
        {"customer_id": 10, "total": 75.5}, {"customer_id": 30, "total": 75.5},
        {"customer_id": 40, "total": 1.0}], out


def test_clean_index_and_input_untouched():
    df = frame()
    before = df.copy()
    out = paid_totals(df)
    assert list(out.index) == [0, 1, 2]
    pd.testing.assert_frame_equal(df, before)


def test_no_paid_rows():
    df = frame()
    df["status"] = "refunded"
    out = paid_totals(df)
    assert len(out) == 0 and list(out.columns) == ["customer_id", "total"]
