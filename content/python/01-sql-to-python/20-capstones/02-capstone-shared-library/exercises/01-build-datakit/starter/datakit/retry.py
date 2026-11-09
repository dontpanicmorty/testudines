"""Retry decorator with exponential backoff."""
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
    raise NotImplementedError
