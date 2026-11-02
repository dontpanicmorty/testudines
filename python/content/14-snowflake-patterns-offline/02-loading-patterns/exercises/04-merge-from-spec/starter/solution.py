"""Generate MERGE statements from a table description."""


def build_merge_sql(table: str, staging: str, keys: list[str], columns: list[str]) -> str:
    ...
