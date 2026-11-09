"""Sinks for loaded rows."""
import csv  # noqa: F401


class Sink:
    def write(self, rows):
        raise NotImplementedError


class MemorySink(Sink):
    pass


class CsvSink(Sink):
    pass
