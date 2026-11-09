def infer_schema(rows: list[dict]) -> dict[str, str]:
    """Infer {column: type_name} from rows. See prompt.md for the rules."""
    seen: dict[str, set[str]] = {}
    for row in rows:
        for column, value in row.items():
            types = seen.setdefault(column, set())
            if value is not None:
                types.add(type(value).__name__)
    schema: dict[str, str] = {}
    for column, types in seen.items():
        if not types:
            schema[column] = "null"
        elif len(types) == 1:
            schema[column] = next(iter(types))
        elif types == {"int", "float"}:
            schema[column] = "float"
        else:
            schema[column] = "str"
    return schema
