"""Incremental-load watermark."""


class Watermark:
    """Tracks the newest processed ISO timestamp; only ever moves forward."""

    def __init__(self, start=None):
        self.value = start

    def is_new(self, ts):
        return self.value is None or ts > self.value

    def advance(self, ts):
        if self.is_new(ts):
            self.value = ts
            return True
        return False

    def __repr__(self):
        return f"Watermark({self.value!r})"
