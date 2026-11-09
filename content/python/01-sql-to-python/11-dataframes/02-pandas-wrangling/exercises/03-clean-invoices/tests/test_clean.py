import io
import math
import pandas as pd
from solution import clean_invoices

CSV = """Invoice #,Customer Name ,AMOUNT,Invoice Date,Status
INV-1,MARGARET LISKOV,100.5,2025-09-26,Paid
INV-2,  barbara liskov ,"$3,291.26",05/26/2025,PAID 
INV-3,Ada Turing,N/A,20 Jun 2025,
INV-1,  margaret liskov ,100.5,2025-09-26, paid
INV-4,Hedy Knuth,,31 Jan 2025,overdue
"""


def raw():
    return pd.read_csv(io.StringIO(CSV))


def test_columns_and_dedupe():
    out = clean_invoices(raw())
    assert list(out.columns) == ["invoice", "customer_name", "amount", "invoice_date", "status"]
    assert out["invoice"].tolist() == ["INV-1", "INV-2", "INV-3", "INV-4"], out


def test_values():
    out = clean_invoices(raw())
    assert out["customer_name"].tolist() == ["Margaret Liskov", "Barbara Liskov", "Ada Turing", "Hedy Knuth"]
    amounts = out["amount"].tolist()
    assert amounts[:2] == [100.5, 3291.26]
    assert math.isnan(amounts[2]) and math.isnan(amounts[3])
    assert out["status"].tolist() == ["paid", "paid", "unknown", "overdue"]
    assert out["invoice_date"].dt.strftime("%Y-%m-%d").tolist() == [
        "2025-09-26", "2025-05-26", "2025-06-20", "2025-01-31"]


def test_dtypes_index_and_no_mutation():
    r = raw()
    before = r.copy()
    out = clean_invoices(r)
    assert str(out["amount"].dtype) == "float64"
    assert str(out["invoice_date"].dtype).startswith("datetime64")
    assert list(out.index) == list(range(len(out)))
    pd.testing.assert_frame_equal(r, before)
