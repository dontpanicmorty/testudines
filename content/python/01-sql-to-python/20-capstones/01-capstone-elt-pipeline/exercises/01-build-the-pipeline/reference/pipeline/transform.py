"""Pure transformation: validated rows in, daily revenue rows out."""
from collections import defaultdict

REVENUE_STATUSES = frozenset({"completed", "shipped"})


def daily_revenue(orders: list[dict], items: list[dict], customers: list[dict]) -> list[dict]:
    region_by_customer = {c["customer_id"]: c["region"] for c in customers}
    qualifying = {o["order_id"]: o for o in orders if o["status"] in REVENUE_STATUSES}
    order_value: dict[int, float] = defaultdict(float)
    for item in items:
        if item["order_id"] in qualifying:
            order_value[item["order_id"]] += item["quantity"] * item["unit_price"]
    groups: dict[tuple[str, str], dict] = {}
    for order_id, order in qualifying.items():
        day = order["placed_at"][:10]
        region = region_by_customer.get(order["customer_id"], "unknown")
        g = groups.setdefault((day, region), {"day": day, "region": region, "orders": 0, "revenue": 0.0})
        g["orders"] += 1
        g["revenue"] += order_value.get(order_id, 0.0)
    out = [dict(g, revenue=round(g["revenue"], 2)) for g in groups.values()]
    return sorted(out, key=lambda r: (r["day"], r["region"]))
