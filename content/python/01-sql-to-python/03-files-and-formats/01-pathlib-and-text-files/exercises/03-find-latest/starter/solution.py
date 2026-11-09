from pathlib import Path


def latest_export(folder):
    files = sorted(Path(folder).glob("orders_*"))
    if not files:
        return None
    return files[-1]
