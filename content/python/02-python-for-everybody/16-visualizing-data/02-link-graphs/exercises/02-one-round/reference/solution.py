def rank_step(links, ranks, damping=0.85):
    n = len(links)
    new = {page: (1 - damping) / n for page in links}
    for page, targets in links.items():
        if targets:
            share = damping * ranks[page] / len(targets)
            for t in targets:
                new[t] += share
        else:
            for p in new:
                new[p] += damping * ranks[page] / n
    return new
