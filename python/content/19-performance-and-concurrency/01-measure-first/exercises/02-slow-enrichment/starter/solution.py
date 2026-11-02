def add_region(orders: list[dict], customers: list[dict]) -> list[dict]:
    out = []
    for o in orders:
        for c in customers:
            if c["customer_id"] == o["customer_id"]:
                out.append({**o, "region": c["region"]})
                break
    return out
