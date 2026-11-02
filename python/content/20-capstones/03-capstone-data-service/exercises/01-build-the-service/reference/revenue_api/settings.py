"""Configuration and other injectable values."""
import os
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Settings:
    db_path: str = "revenue.duckdb"
    default_page_size: int = 20
    max_page_size: int = 100


def get_settings() -> Settings:
    """Read settings from REVENUE_DB_PATH, REVENUE_DEFAULT_PAGE_SIZE, REVENUE_MAX_PAGE_SIZE."""
    defaults = Settings()
    return Settings(
        db_path=os.environ.get("REVENUE_DB_PATH", defaults.db_path),
        default_page_size=int(os.environ.get("REVENUE_DEFAULT_PAGE_SIZE", defaults.default_page_size)),
        max_page_size=int(os.environ.get("REVENUE_MAX_PAGE_SIZE", defaults.max_page_size)),
    )


def get_today() -> date:
    """Today's date, as a dependency so tests can pin it."""
    return date.today()
