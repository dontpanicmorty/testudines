"""Sinks for loaded rows."""
import csv
from abc import ABC, abstractmethod


class Sink(ABC):
    @abstractmethod
    def write(self, rows):
        """Persist rows and return how many were written."""


class MemorySink(Sink):
    def __init__(self):
        self.rows = []

    def write(self, rows):
        self.rows.extend(rows)
        return len(rows)


class CsvSink(Sink):
    def __init__(self, path):
        self.path = path

    def write(self, rows):
        if not rows:
            return 0
        with open(self.path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        return len(rows)
