from pathlib import Path
from typing import Iterator


def read_in_chunks(path: str | Path, size: int) -> Iterator[list[dict]]:
    raise NotImplementedError
