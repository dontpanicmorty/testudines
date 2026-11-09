"""A composable ETL pipeline."""
from dataclasses import dataclass


@dataclass(frozen=True)
class RunResult:
    rows_in: int
    rows_out: int
    rejected: int


class Pipeline:
    def __init__(self, extract, transform, load):
        self.extract = extract
        self.transform = transform
        self.load = load

    def run(self):
        rows_in = 0
        good = []
        for row in self.extract():
            rows_in += 1
            try:
                out = self.transform(row)
            except ValueError:
                continue
            if out is not None:
                good.append(out)
        stored = self.load(good)
        return RunResult(rows_in, stored, rows_in - len(good))
