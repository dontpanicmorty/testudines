STATUSES = {"paid", "open", "void"}


def clean_orders(rows, seen_ids=None):
    seen = set() if seen_ids is None else set(seen_ids)
    out = []
    for row in rows:
        order_id = row.get("order_id")
        if not isinstance(order_id, str) or not order_id.strip():
            raise ValueError(f"order_id required, got {order_id!r}")
        qty = int(row["quantity"])
        if qty <= 0:
            raise ValueError(f"quantity must be positive, got {qty}")
        status_raw = row.get("status")
        status = status_raw.strip().lower() if isinstance(status_raw, str) else ""
        if status not in STATUSES:
            raise ValueError(f"bad status {status_raw!r}")
        if order_id in seen:
            continue
        seen.add(order_id)
        out.append({"order_id": order_id, "quantity": qty, "status": status})
    return out
