"""A non-integer timeout raises ValueError instead of ConfigError."""
import os


class ConfigError(Exception):
    """Raised for missing or invalid configuration."""


def connection_settings():
    """Read DOJO_WAREHOUSE (required), DOJO_SCHEMA and DOJO_TIMEOUT (positive int)."""
    warehouse = os.environ.get("DOJO_WAREHOUSE", "").strip()
    if not warehouse:
        raise ConfigError("DOJO_WAREHOUSE is required")
    raw_timeout = os.environ.get("DOJO_TIMEOUT", "30")
    try:
        timeout = int(raw_timeout)
    except ValueError:
        raise
    if timeout <= 0:
        raise ConfigError("DOJO_TIMEOUT must be positive")
    return {
        "warehouse": warehouse,
        "schema": os.environ.get("DOJO_SCHEMA", "analytics"),
        "timeout": timeout,
    }
