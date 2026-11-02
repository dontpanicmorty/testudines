"""Database access behind a small protocol."""
import sqlite3
from contextlib import contextmanager
from typing import Any, Iterator, Protocol, Sequence, runtime_checkable

from .errors import DatabaseError


@runtime_checkable
class ConnectionProtocol(Protocol):
    """What datakit (and consumers) need from a database connection."""

    def query(self, sql: str, params: Sequence[Any] = ()) -> list[dict]: ...

    def execute(self, sql: str, params: Sequence[Any] = ()) -> int: ...

    def close(self) -> None: ...


class SqliteConnection:
    """sqlite3-backed implementation of ConnectionProtocol."""

    def __init__(self, path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._depth = 0

    def query(self, sql: str, params: Sequence[Any] = ()) -> list[dict]:
        try:
            return [dict(r) for r in self._conn.execute(sql, tuple(params)).fetchall()]
        except sqlite3.Error as exc:
            raise DatabaseError(str(exc)) from exc

    def execute(self, sql: str, params: Sequence[Any] = ()) -> int:
        try:
            cur = self._conn.execute(sql, tuple(params))
            if self._depth == 0:
                self._conn.commit()
            return cur.rowcount
        except sqlite3.Error as exc:
            raise DatabaseError(str(exc)) from exc

    def executemany(self, sql: str, rows: Sequence[Sequence[Any]]) -> int:
        try:
            cur = self._conn.executemany(sql, [tuple(r) for r in rows])
            if self._depth == 0:
                self._conn.commit()
            return cur.rowcount
        except sqlite3.Error as exc:
            raise DatabaseError(str(exc)) from exc

    @contextmanager
    def transaction(self) -> Iterator["SqliteConnection"]:
        if self._depth > 0:
            yield self                      # nested: the outer transaction owns commit/rollback
            return
        self._depth = 1
        try:
            yield self
        except BaseException:
            self._conn.rollback()
            raise
        else:
            self._conn.commit()
        finally:
            self._depth = 0

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "SqliteConnection":
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()
