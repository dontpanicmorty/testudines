"""Retry decorator with exponential backoff."""
import functools
import time
from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable)


def retry(
    attempts: int = 3,
    delay: float = 0.0,
    backoff: float = 2.0,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    sleep: Callable[[float], None] = time.sleep,
) -> Callable[[F], F]:
    """Retry the decorated function when it raises one of ``exceptions``.

    Waits ``delay * backoff**n`` seconds before retry n+1. After the last attempt the
    original exception is re-raised unchanged.
    """
    if attempts < 1:
        raise ValueError("attempts must be >= 1")
    if delay < 0 or backoff < 1:
        raise ValueError("delay must be >= 0 and backoff >= 1")

    def decorator(fn: F) -> F:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except exceptions:
                    if attempt == attempts - 1:
                        raise
                    sleep(delay * backoff**attempt)

        return wrapper  # type: ignore[return-value]

    return decorator
