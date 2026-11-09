import csv
from pathlib import Path
from typing import Iterator


def read_in_chunks(path: str | Path, size: int) -> Iterator[list[dict]]:
    if size < 1:
        raise ValueError("size must be >= 1")
    with open(path, newline="") as f:
        batch: list[dict] = []
        for row in csv.DictReader(f):
            batch.append(row)
            if len(batch) == size:
                yield batch
                batch = []
        if batch:
            yield batch
