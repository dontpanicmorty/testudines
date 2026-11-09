def check_orders(rows):
    if not rows:
        return ["empty"]
    problems = []
    ids = [r.get("order_id") for r in rows]
    if any(i is None for i in ids):
        problems.append("null_order_id")
    present = [i for i in ids if i is not None]
    if len(present) != len(set(present)):
        problems.append("duplicate_order_id")
    for r in rows:
        a = r.get("amount")
        if isinstance(a, bool) or not isinstance(a, (int, float)) or a < 0:
            problems.append("bad_amount")
            break
    return problems
