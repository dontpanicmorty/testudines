from typing import Callable

Handler = Callable[..., tuple[int, dict]]


def _segments(path: str) -> list[str]:
    return [s for s in path.strip("/").split("/")] if path.strip("/") else []


class Router:
    def __init__(self) -> None:
        self._routes: list[tuple[str, list[str], Handler]] = []

    def add(self, method: str, pattern: str, handler: Handler) -> None:
        self._routes.append((method.upper(), _segments(pattern), handler))

    @staticmethod
    def _match(pattern: list[str], parts: list[str]) -> dict[str, str] | None:
        if len(pattern) != len(parts):
            return None
        params: dict[str, str] = {}
        for pat, part in zip(pattern, parts):
            if pat.startswith("{") and pat.endswith("}"):
                params[pat[1:-1]] = part
            elif pat != part:
                return None
        return params

    def dispatch(self, method: str, path: str) -> tuple[int, dict]:
        parts = _segments(path)
        matches = []
        for m, pattern, handler in self._routes:
            params = self._match(pattern, parts)
            if params is not None:
                literals = sum(1 for p in pattern if not p.startswith("{"))
                matches.append((literals, m, handler, params))
        if not matches:
            return 404, {"error": "not found"}
        matches.sort(key=lambda t: -t[0])
        for _, m, handler, params in matches:
            if m == method.upper():
                return handler(**params)
        return 405, {"error": "method not allowed"}
