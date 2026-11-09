import time

import httpx


class RetryExhausted(Exception):
    """All attempts failed."""


def get_with_retries(client: httpx.Client, path: str, max_attempts: int = 4, sleep=time.sleep):
    last: str = "no attempts made"
    for attempt in range(max_attempts):
        wait = 0.5 * 2 ** attempt
        try:
            resp = client.get(path)
        except httpx.TransportError as exc:
            last = f"transport error: {exc}"
        else:
            if resp.is_success:
                return resp.json()
            if resp.status_code == 429:
                retry_after = resp.headers.get("Retry-After")
                if retry_after is not None:
                    wait = float(retry_after)
                last = "rate limited"
            elif resp.status_code >= 500:
                last = f"server error {resp.status_code}"
            else:
                resp.raise_for_status()
        if attempt < max_attempts - 1:
            sleep(wait)
    raise RetryExhausted(f"{path}: {last} after {max_attempts} attempts")
