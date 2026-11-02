"""A composable ETL pipeline."""
from dataclasses import dataclass


@dataclass(frozen=True)
class RunResult:
    rows_in: int
    rows_out: int
    rejected: int


class Pipeline:
    pass
