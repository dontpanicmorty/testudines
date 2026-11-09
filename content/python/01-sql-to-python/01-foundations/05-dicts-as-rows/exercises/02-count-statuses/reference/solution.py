def summarise(orders):
    out = {}
    for o in orders:
        entry = out.setdefault(o["status"], {"count": 0, "total": 0.0})
        entry["count"] += 1
        entry["total"] += o["amount"]
    return {k: {"count": v["count"], "total": round(v["total"], 2)} for k, v in out.items()}
