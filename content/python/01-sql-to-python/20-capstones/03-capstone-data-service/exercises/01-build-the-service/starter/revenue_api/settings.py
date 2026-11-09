"""Configuration and other injectable values."""
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Settings:
    db_path: str = "revenue.duckdb"
    default_page_size: int = 20
    max_page_size: int = 100


def get_settings() -> Settings:
    """Read settings from REVENUE_DB_PATH, REVENUE_DEFAULT_PAGE_SIZE, REVENUE_MAX_PAGE_SIZE.

    Missing variables fall back to the Settings defaults.
    """
    raise NotImplementedError


def get_today() -> date:
    """Today's date, as a dependency so tests can pin it."""
    return date.today()
