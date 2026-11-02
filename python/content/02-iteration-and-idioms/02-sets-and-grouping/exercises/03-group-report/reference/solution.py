from collections import defaultdict


def revenue_report(orders):
    groups = defaultdict(list)
    for o in orders:
        groups[(o["region"], o["plan"])].append(o["amount"])
    return [
        {
            "region": region,
            "plan": plan,
            "orders": len(vals),
            "revenue": round(sum(vals), 2),
            "avg": round(sum(vals) / len(vals), 2),
        }
        for (region, plan), vals in sorted(groups.items())
    ]
