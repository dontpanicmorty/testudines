"""A scripted fake of a Snowflake-style connection."""


class FakeCursor:
    def __init__(self, conn):
        self._conn = conn
        self._rows: list[tuple] = []
        self._pos = 0
        self.description = None
        self.rowcount = -1
        self.closed = False

    def execute(self, sql, params=None):
        self._conn.executed.append((sql, params))
        if not self._conn._script:
            raise RuntimeError(f"no scripted result for: {sql}")
        result = self._conn._script.pop(0)
        if result:
            names = list(result[0].keys())
            self.description = [(n.upper(), None, None, None, None, None, None) for n in names]
            self._rows = [tuple(r[n] for n in names) for r in result]
        else:
            self.description = None
            self._rows = []
        self._pos = 0
        self.rowcount = len(result)
        return self

    def fetchone(self):
        if self._pos >= len(self._rows):
            return None
        row = self._rows[self._pos]
        self._pos += 1
        return row

    def fetchmany(self, size=1):
        chunk = self._rows[self._pos:self._pos + size]
        self._pos += len(chunk)
        return chunk

    def fetchall(self):
        chunk = self._rows[self._pos:]
        self._pos = len(self._rows)
        return chunk

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


class FakeConnection:
    def __init__(self, script):
        self._script = [list(rs) for rs in script]
        self.executed: list[tuple] = []
        self.commits = 0
        self.closed = False

    def cursor(self):
        return FakeCursor(self)

    def commit(self):
        self.commits += 1

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False
