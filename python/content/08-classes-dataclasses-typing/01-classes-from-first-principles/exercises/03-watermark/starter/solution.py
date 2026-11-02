"""Incremental-load watermark."""


class Watermark:
    """Tracks the newest processed ISO timestamp; only ever moves forward."""
