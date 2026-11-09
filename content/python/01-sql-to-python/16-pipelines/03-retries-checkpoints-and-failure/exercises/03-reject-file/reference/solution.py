import json
from pathlib import Path


class TooManyRejects(Exception):
    pass


def load_rows(rows, parse, reject_path, max_reject_rate=0.2):
    good, rejects = [], []
    for raw in rows:
        try:
            good.append(parse(raw))
        except ValueError as exc:
            rejects.append({"row": raw, "error": str(exc)})
    path = Path(reject_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as fh:
        for r in rejects:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    if rows and len(rejects) / len(rows) > max_reject_rate:
        raise TooManyRejects(f"{len(rejects)} of {len(rows)} rows rejected")
    return good
