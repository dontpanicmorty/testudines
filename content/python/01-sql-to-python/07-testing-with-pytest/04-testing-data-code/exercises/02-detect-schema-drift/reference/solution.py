"""Schema drift detection."""


def check_schema(expected, actual):
    problems = []
    for name in sorted(set(expected) | set(actual)):
        if name not in actual:
            problems.append(f"missing column: {name}")
        elif name not in expected:
            problems.append(f"unexpected column: {name}")
        elif expected[name] != actual[name]:
            problems.append(f"type changed: {name} {expected[name]} -> {actual[name]}")
    return problems
