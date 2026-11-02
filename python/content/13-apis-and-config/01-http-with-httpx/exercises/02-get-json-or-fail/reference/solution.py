import httpx


class ApiError(Exception):
    def __init__(self, status_code, message=""):
        super().__init__(message or f"API error (status={status_code})")
        self.status_code = status_code


def get_json(client: httpx.Client, path: str):
    try:
        resp = client.get(path)
    except httpx.HTTPError as exc:
        raise ApiError(None, str(exc)) from exc
    if not resp.is_success:
        raise ApiError(resp.status_code, f"{path} returned {resp.status_code}")
    return resp.json()
