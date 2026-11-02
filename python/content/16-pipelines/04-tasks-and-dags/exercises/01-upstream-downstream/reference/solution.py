def downstream(graph, node):
    dependents = {n: [] for n in graph}
    for n, deps in graph.items():
        for d in deps:
            dependents.setdefault(d, []).append(n)
    seen = set()
    stack = list(dependents.get(node, []))
    while stack:
        n = stack.pop()
        if n not in seen:
            seen.add(n)
            stack.extend(dependents.get(n, []))
    return seen
