def orphan_order_ids(orders: list[dict], customers: list[dict]) -> list[int]:
    known = {c["customer_id"] for c in customers}
    return sorted({o["order_id"] for o in orders if o["customer_id"] not in known})
