import csv
import sqlite3
from decimal import Decimal, InvalidOperation


def read_valid(path):
    valid, rejects = [], []
    with open(path, newline="", encoding="utf-8") as f:
        for line_no, raw in enumerate(csv.DictReader(f), start=2):
            try:
                customer_id = int(raw["customer_id"])
                quantity = int(raw["quantity"])
                unit_price = Decimal(raw["unit_price"])
                if not raw["order_id"].strip() or not raw["sku"].strip():
                    raise ValueError("order_id and sku are required")
                if quantity <= 0 or unit_price < 0:
                    raise ValueError("quantity must be positive and unit_price not negative")
            except (ValueError, InvalidOperation) as e:
                rejects.append({"line": line_no, "reason": str(e)})
                continue
            valid.append(
                {
                    "order_id": raw["order_id"].strip(),
                    "customer_id": customer_id,
                    "sku": raw["sku"].strip().upper(),
                    "quantity": quantity,
                    "unit_price": unit_price,
                }
            )
    return valid, rejects


def customer_totals(lines):
    out = {}
    for r in lines:
        t = out.setdefault(
            r["customer_id"],
            {"customer_id": r["customer_id"], "line_count": 0, "revenue": Decimal("0")},
        )
        t["line_count"] += 1
        t["revenue"] += r["quantity"] * r["unit_price"]
    return [out[k] for k in sorted(out)]


def run_etl(src, db_path, reject_path):
    # TODO: dedupe, load into sqlite (idempotent), write rejects, return counts
    return {}
