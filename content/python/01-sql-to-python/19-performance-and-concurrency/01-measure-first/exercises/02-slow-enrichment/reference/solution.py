def add_region(orders: list[dict], customers: list[dict]) -> list[dict]:
    region_by_id: dict = {}
    for c in customers:
        region_by_id.setdefault(c["customer_id"], c["region"])   # first match wins, as before
    return [
        {**o, "region": region_by_id[o["customer_id"]]}
        for o in orders
        if o["customer_id"] in region_by_id
    ]
