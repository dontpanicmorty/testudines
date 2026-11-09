import pandas as pd
from solution import parse_dates


def test_three_formats_and_bad():
    out = parse_dates(pd.Series(["2025-09-26", "05/26/2025", "20 Jun 2025", "oops", None]))
    assert out.dt.strftime("%Y-%m-%d").tolist()[:3] == ["2025-09-26", "2025-05-26", "2025-06-20"]
    assert out.isna().tolist() == [False, False, False, True, True]


def test_ambiguous_is_month_first():
    out = parse_dates(pd.Series(["03/04/2025"]))
    assert out.iloc[0] == pd.Timestamp(2025, 3, 4)


def test_dtype_and_index():
    out = parse_dates(pd.Series(["2025-01-02"], index=[7]))
    assert str(out.dtype).startswith("datetime64")
    assert list(out.index) == [7]


def test_whitespace_tolerated():
    assert parse_dates(pd.Series([" 2025-01-02 "])).iloc[0] == pd.Timestamp(2025, 1, 2)
