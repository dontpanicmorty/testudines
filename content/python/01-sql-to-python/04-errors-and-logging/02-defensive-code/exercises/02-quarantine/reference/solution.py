class TooManyRejects(RuntimeError):
    pass


def process(rows, validate, max_reject_rate=0.05):
    good, rejected = [], []
    for n, raw in enumerate(rows, start=1):
        try:
            good.append(validate(raw))
        except ValueError as e:
            rejected.append({"row": n, "reason": str(e), "raw": raw})
    if rows and len(rejected) / len(rows) > max_reject_rate:
        raise TooManyRejects(f"{len(rejected)}/{len(rows)} rows rejected")
    return good, rejected
