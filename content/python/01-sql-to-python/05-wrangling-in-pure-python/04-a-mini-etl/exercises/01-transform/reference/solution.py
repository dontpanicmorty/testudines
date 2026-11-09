from decimal import Decimal


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
