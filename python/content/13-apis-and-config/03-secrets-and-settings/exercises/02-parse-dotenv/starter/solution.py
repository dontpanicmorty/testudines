"""Minimal .env parser: no third-party libraries."""


def parse_dotenv(text: str) -> dict[str, str]:
    ...
