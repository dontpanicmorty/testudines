def enrich_orders(orders, customers):
    by_id = {c["customer_id"]: c for c in customers}
    out = []
    for o in orders:
        cust = by_id.get(o["customer_id"], {})
        out.append({**o, "region": cust.get("region"), "plan": cust.get("plan")})
    return out
