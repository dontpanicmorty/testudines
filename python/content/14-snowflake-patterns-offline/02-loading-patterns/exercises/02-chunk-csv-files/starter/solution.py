import csv
from collections.abc import Iterable
from pathlib import Path


def write_chunks(rows: Iterable[dict], out_dir: Path, prefix: str, max_rows: int,
                 fieldnames: list[str]) -> list[Path]:
    # Currently writes everything to a single file.
    path = Path(out_dir) / f"{prefix}_0001.csv"
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    return [path]
