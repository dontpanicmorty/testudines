from pathlib import Path


def count_records(path: Path) -> int:
    n = 0
    with Path(path).open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                n += 1
    return n
