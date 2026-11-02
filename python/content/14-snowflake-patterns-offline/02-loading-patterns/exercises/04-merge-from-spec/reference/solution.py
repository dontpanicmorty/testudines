"""Generate MERGE statements from a table description."""


def build_merge_sql(table: str, staging: str, keys: list[str], columns: list[str]) -> str:
    if not columns:
        raise ValueError("columns must not be empty")
    if not keys:
        raise ValueError("at least one key is required")
    missing = [k for k in keys if k not in columns]
    if missing:
        raise ValueError(f"keys not in columns: {missing}")
    on = " AND ".join(f"tgt.{k} = src.{k}" for k in keys)
    sets = ", ".join(f"tgt.{c} = src.{c}" for c in columns if c not in keys)
    parts = [f"MERGE INTO {table} AS tgt USING {staging} AS src ON {on}"]
    if sets:
        parts.append(f"WHEN MATCHED THEN UPDATE SET {sets}")
    cols = ", ".join(columns)
    vals = ", ".join(f"src.{c}" for c in columns)
    parts.append(f"WHEN NOT MATCHED THEN INSERT ({cols}) VALUES ({vals})")
    return " ".join(parts)
