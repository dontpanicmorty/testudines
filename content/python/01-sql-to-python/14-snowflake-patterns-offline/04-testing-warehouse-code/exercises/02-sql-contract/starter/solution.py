"""SQL builders whose output is easy to assert on."""


def build_select(table: str, columns: list[str], filters: dict | None = None) -> tuple[str, dict]:
    ...
