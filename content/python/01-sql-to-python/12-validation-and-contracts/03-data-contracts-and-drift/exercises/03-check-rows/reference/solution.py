def check_rows(contract: dict[str, str], rows: list[dict]) -> list[tuple[int, str, str]]:
    """Return sorted (row_index, column, problem) violations."""
    violations: list[tuple[int, str, str]] = []
    for index, row in enumerate(rows):
        for column, expected in contract.items():
            if column not in row:
                violations.append((index, column, "missing"))
                continue
            value = row[column]
            if value is None:
                continue
            actual = type(value).__name__
            if actual != expected and not (expected == "float" and actual == "int"):
                violations.append((index, column, "wrong_type"))
        for column in row:
            if column not in contract:
                violations.append((index, column, "unexpected"))
    return sorted(violations)
