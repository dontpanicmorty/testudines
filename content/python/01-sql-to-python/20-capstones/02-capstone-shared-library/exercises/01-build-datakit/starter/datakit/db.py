"""Database access behind a small protocol."""
from typing import Any, Protocol, Sequence, runtime_checkable

from .errors import DatabaseError


@runtime_checkable
class ConnectionProtocol(Protocol):
    """What datakit (and consumers) need from a database connection."""

    def query(self, sql: str, params: Sequence[Any] = ()) -> list[dict]: ...

    def execute(self, sql: str, params: Sequence[Any] = ()) -> int: ...

    def close(self) -> None: ...


class SqliteConnection:
    """sqlite3-backed implementation of ConnectionProtocol.

    Also provides executemany(sql, rows), transaction() as a context manager, and
    use as a context manager that closes the connection.
    """

    def __init__(self, path: str = ":memory:") -> None:
        raise NotImplementedError
