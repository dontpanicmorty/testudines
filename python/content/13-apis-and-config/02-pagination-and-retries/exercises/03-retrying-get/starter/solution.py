import time

import httpx


class RetryExhausted(Exception):
    """All attempts failed."""


def get_with_retries(client: httpx.Client, path: str, max_attempts: int = 4, sleep=time.sleep):
    resp = client.get(path)
    resp.raise_for_status()
    return resp.json()
