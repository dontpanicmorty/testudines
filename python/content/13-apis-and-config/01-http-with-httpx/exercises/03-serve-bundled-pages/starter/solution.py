"""Build a fake users API from bundled JSON files and walk its pages."""
from pathlib import Path

import httpx


def make_mock_client(data_dir: Path) -> httpx.Client:
    ...


def active_names(client: httpx.Client) -> list[str]:
    ...
