"""Orchestration: extract, validate, transform, load."""
import csv
import logging
from pathlib import Path

from . import load, schema, transform

log = logging.getLogger("pipeline")


def read_csv_rows(path: Path) -> list[dict]:
    raise NotImplementedError


def run_pipeline(data_dir: str | Path, db_path: str | Path, incremental: bool = False) -> dict:
    """Run the whole pipeline and return the stats dict described in the brief."""
    raise NotImplementedError
