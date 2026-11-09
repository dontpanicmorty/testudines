def infer_schema(rows: list[dict]) -> dict[str, str]:
    """Infer {column: type_name} from rows. See prompt.md for the rules."""
