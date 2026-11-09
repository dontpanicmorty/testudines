import json


def graph_json(links, rounds=20, damping=0.85):
    n = len(links)
    ranks = {p: 1 / n for p in links} if n else {}
    for _ in range(rounds):
        new = {p: (1 - damping) / n for p in links}
        for page, targets in links.items():
            if targets:
                share = damping * ranks[page] / len(targets)
                for t in targets:
                    new[t] += share
            else:
                for p in new:
                    new[p] += damping * ranks[page] / n
        ranks = new
    nodes = [{"id": p, "rank": round(ranks[p], 4)} for p in sorted(links)]
    edges = [{"source": a, "target": b} for a in sorted(links) for b in sorted(links[a])]
    return json.dumps({"nodes": nodes, "links": edges})
