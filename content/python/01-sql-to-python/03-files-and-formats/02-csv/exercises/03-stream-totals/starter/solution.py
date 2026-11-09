import csv


def revenue_by_product(path):
    totals = {}
    with open(path, newline="", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        first = next(rows)               # peek at the first row
        totals[first["product_id"]] = first["quantity"] * first["unit_price"]
        for row in rows:
            key = row["product_id"]
            totals[key] = totals.get(key, 0) + row["quantity"] * row["unit_price"]
    return totals
