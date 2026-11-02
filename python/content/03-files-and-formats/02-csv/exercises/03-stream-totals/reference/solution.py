import csv


def revenue_by_product(path):
    totals = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = row["product_id"]
            line = int(row["quantity"]) * float(row["unit_price"])
            totals[key] = totals.get(key, 0.0) + line
    return totals
