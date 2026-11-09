import csv


def read_order_lines(path):
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out.append(
                {
                    "order_id": int(row["order_id"]),
                    "product_id": row["product_id"],
                    "quantity": int(row["quantity"]),
                    "unit_price": float(row["unit_price"]),
                }
            )
    return out
