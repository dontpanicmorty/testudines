def clean_orders(rows, seen_ids=[]):
    out = []
    for row in rows:
        assert row["order_id"], "order_id required"
        qty = int(row["quantity"])
        assert qty > 0, "quantity must be positive"
        status = str(row.get("status")).lower()
        assert status in ("paid", "open", "void"), "bad status"
        if row["order_id"] in seen_ids:
            continue
        seen_ids.append(row["order_id"])
        out.append({"order_id": row["order_id"], "quantity": qty, "status": status})
    return out
