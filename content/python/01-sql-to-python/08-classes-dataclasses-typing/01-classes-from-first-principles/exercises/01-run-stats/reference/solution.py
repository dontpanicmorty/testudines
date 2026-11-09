"""Run statistics."""


class RunStats:
    def __init__(self):
        self.rows_read = 0
        self.rows_rejected = 0

    def record(self, ok):
        self.rows_read += 1
        if not ok:
            self.rows_rejected += 1

    @property
    def reject_rate(self):
        return self.rows_rejected / self.rows_read if self.rows_read else 0.0

    def __repr__(self):
        return f"RunStats(read={self.rows_read}, rejected={self.rows_rejected})"
