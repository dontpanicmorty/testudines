def topo_sort(graph):
    for node, deps in graph.items():
        for d in deps:
            if d not in graph:
                raise ValueError(f"{node!r} depends on undefined node {d!r}")
    remaining = {n: set(deps) for n, deps in graph.items()}
    order = []
    while remaining:
        ready = sorted(n for n, deps in remaining.items() if not deps)
        if not ready:
            raise ValueError(f"cycle among: {sorted(remaining)}")
        node = ready[0]
        order.append(node)
        del remaining[node]
        for deps in remaining.values():
            deps.discard(node)
    return order
