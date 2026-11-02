import re

import pandas as pd

FORMATS = ["%Y-%m-%d", "%m/%d/%Y", "%d %b %Y"]


def _norm(col: str) -> str:
    key = re.sub(r"[^a-z0-9]+", "_", col.strip().lower()).strip("_")
    return {"invoice": "invoice", "customer_name": "customer_name", "amount": "amount",
            "invoice_date": "invoice_date", "status": "status"}[key]


def _dates(s: pd.Series) -> pd.Series:
    text = s.astype("string").str.strip()
    out = pd.to_datetime(text, format=FORMATS[0], errors="coerce")
    for fmt in FORMATS[1:]:
        out = out.fillna(pd.to_datetime(text, format=fmt, errors="coerce"))
    return out


def clean_invoices(raw: pd.DataFrame) -> pd.DataFrame:
    """Tidy the invoice export. See prompt.md."""
    df = raw.rename(columns=_norm)
    amount = df["amount"].astype("string").str.strip().str.replace(r"[$,]", "", regex=True)
    out = pd.DataFrame({
        "invoice": df["invoice"].astype("string").str.strip(),
        "customer_name": df["customer_name"].astype("string").str.strip().str.title(),
        "amount": pd.to_numeric(amount, errors="coerce").astype("float64"),
        "invoice_date": _dates(df["invoice_date"]),
        "status": df["status"].astype("string").str.strip().str.lower().fillna("unknown"),
    })
    return out.drop_duplicates().reset_index(drop=True)
