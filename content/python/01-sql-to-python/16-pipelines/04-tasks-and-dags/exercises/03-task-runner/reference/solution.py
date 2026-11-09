def _order(names, deps):
    remaining = {n: set(deps.get(n, [])) & set(names) for n in names}
    order = []
    while remaining:
        ready = sorted(n for n, d in remaining.items() if not d)
        if not ready:
            raise ValueError(f"cycle among: {sorted(remaining)}")
        node = ready[0]
        order.append(node)
        del remaining[node]
        for d in remaining.values():
            d.discard(node)
    return order


def run_tasks(tasks, deps):
    order = _order(list(tasks), deps)
    status = {}
    for name in order:
        needed = [d for d in deps.get(name, []) if d in tasks]
        if any(status[d] != "success" for d in needed):
            status[name] = "skipped"
            continue
        try:
            tasks[name]()
            status[name] = "success"
        except Exception:
            status[name] = "failed"
    return status
