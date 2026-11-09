import csv
import re
from datetime import datetime
from decimal import Decimal

FORMATS = ("%Y-%m-%d", "%d %b %Y", "%m/%d/%Y")


def _norm_header(h):
    return re.sub(r"[^a-z0-9]+", "_", h.strip().lower()).strip("_")


def _amount(text):
    text = (text or "").strip()
    if text == "" or text.upper() == "N/A":
        return None
    return Decimal(text.replace("$", "").replace(",", ""))


def _date(text):
    text = text.strip()
    for fmt in FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"unrecognised date: {text!r}")


def clean_invoices(path):
    out, seen = [], set()
    with open(path, newline="", encoding="utf-8") as f:
        for raw in csv.DictReader(f):
            row = {_norm_header(k): v for k, v in raw.items()}
            invoice_id = row["invoice"].strip()
            if invoice_id in seen:
                continue
            seen.add(invoice_id)
            status = (row["status"] or "").strip().lower()
            out.append(
                {
                    "invoice_id": invoice_id,
                    "customer": row["customer_name"].strip().title(),
                    "amount": _amount(row["amount"]),
                    "invoice_date": _date(row["invoice_date"]),
                    "status": status or None,
                }
            )
    return out
