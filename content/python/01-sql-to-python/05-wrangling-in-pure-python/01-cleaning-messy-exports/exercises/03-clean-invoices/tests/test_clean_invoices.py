import csv
import os
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from solution import clean_invoices

SRC = (
    "Invoice #,Customer Name ,AMOUNT,Invoice Date,Status\n"
    'INV-1,  ada turing ,"$3,291.26",2025-05-20,PAID \n'
    "INV-2,MARGARET LISKOV,N/A,20 Jun 2025,\n"
    "INV-1,Ada Turing,1.00,2025-05-21,open\n"
    "INV-3,Hedy Knuth,,05/26/2025,paid\n"
)


def test_small_file(tmp_path):
    p = tmp_path / "inv.csv"
    p.write_text(SRC, encoding="utf-8")
    out = clean_invoices(p)
    assert out == [
        {"invoice_id": "INV-1", "customer": "Ada Turing", "amount": Decimal("3291.26"),
         "invoice_date": date(2025, 5, 20), "status": "paid"},
        {"invoice_id": "INV-2", "customer": "Margaret Liskov", "amount": None,
         "invoice_date": date(2025, 6, 20), "status": None},
        {"invoice_id": "INV-3", "customer": "Hedy Knuth", "amount": None,
         "invoice_date": date(2025, 5, 26), "status": "paid"},
    ]


def test_bundled_file_invariants():
    path = Path(os.environ["DOJO_DATA"]) / "messy_invoices.csv"
    with path.open(newline="", encoding="utf-8") as f:
        raw_ids = [r["Invoice #"].strip() for r in csv.DictReader(f)]
    out = clean_invoices(path)
    assert [r["invoice_id"] for r in out] == list(dict.fromkeys(raw_ids))
    for r in out:
        assert set(r) == {"invoice_id", "customer", "amount", "invoice_date", "status"}
        assert r["amount"] is None or isinstance(r["amount"], Decimal)
        assert isinstance(r["invoice_date"], date) and not isinstance(r["invoice_date"], datetime)
        assert r["status"] is None or r["status"] == r["status"].strip().lower()
        assert r["customer"] == r["customer"].strip()
