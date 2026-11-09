from pathlib import Path


def latest_export(folder):
    best = None
    best_n = -1
    for p in Path(folder).glob("orders_*.csv"):
        tail = p.stem[len("orders_"):]
        if not tail.isdigit():
            continue
        if int(tail) > best_n:
            best, best_n = p, int(tail)
    return best
