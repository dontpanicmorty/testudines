"""Exception hierarchy: consumers can catch DatakitError to handle anything we raise."""


class DatakitError(Exception):
    """Base class for every error raised by datakit."""


class ConfigError(DatakitError):
    """Configuration is missing or invalid. ``errors`` lists every problem found."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


class DatabaseError(DatakitError):
    """A database operation failed. The original exception is chained as __cause__."""
