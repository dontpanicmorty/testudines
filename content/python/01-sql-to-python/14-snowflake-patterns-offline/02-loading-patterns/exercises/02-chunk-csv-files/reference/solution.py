import csv
from collections.abc import Iterable
from pathlib import Path


def write_chunks(rows: Iterable[dict], out_dir: Path, prefix: str, max_rows: int,
                 fieldnames: list[str]) -> list[Path]:
    if max_rows < 1:
        raise ValueError("max_rows must be >= 1")
    out_dir = Path(out_dir)
    paths: list[Path] = []
    handle = None
    writer = None
    count = 0
    try:
        for row in rows:
            if handle is None or count == max_rows:
                if handle is not None:
                    handle.close()
                path = out_dir / f"{prefix}_{len(paths) + 1:04d}.csv"
                paths.append(path)
                handle = path.open("w", newline="")
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                count = 0
            writer.writerow(row)
            count += 1
    finally:
        if handle is not None:
            handle.close()
    return paths
