def add_window_columns(orders):
    ordered = sorted(orders, key=lambda r: (r["customer"], r["day"]))
    out = []
    current = object()
    running, prev = 0, None
    for r in ordered:
        if r["customer"] != current:
            current = r["customer"]
            running, prev = 0, None
        running += r["amount"]
        out.append({**r, "running_total": running, "prev_amount": prev})
        prev = r["amount"]
    return out
