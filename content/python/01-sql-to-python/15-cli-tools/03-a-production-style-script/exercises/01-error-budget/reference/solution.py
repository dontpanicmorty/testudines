def evaluate(total: int, rejected: int, max_error_rate: float) -> tuple[int, str]:
    if rejected < 0 or rejected > total:
        raise ValueError("rejected must be between 0 and total")
    if not 0 <= max_error_rate <= 1:
        raise ValueError("max_error_rate must be between 0 and 1")
    if total == 0:
        return 1, "no input rows"
    rate = rejected / total
    if rate > max_error_rate:
        return 1, f"error rate {rate:.1%} exceeds budget of {max_error_rate:.1%}"
    return 0, f"ok: {rejected} of {total} rows rejected"
