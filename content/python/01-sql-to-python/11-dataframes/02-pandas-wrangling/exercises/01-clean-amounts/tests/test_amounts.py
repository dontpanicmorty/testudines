import math
import pandas as pd
from solution import clean_amounts


def test_values():
    out = clean_amounts(pd.Series(["$1,000.50", " 7 ", "N/A", "", None, "12.25"]))
    vals = out.tolist()
    assert vals[0] == 1000.5 and vals[1] == 7.0 and vals[5] == 12.25
    assert all(math.isnan(v) for v in vals[2:5]), vals


def test_dtype_and_index():
    s = pd.Series(["1", "2"], index=[5, 9])
    out = clean_amounts(s)
    assert str(out.dtype) == "float64"
    assert list(out.index) == [5, 9]


def test_no_zero_fill():
    assert clean_amounts(pd.Series(["N/A"])).isna().all()
