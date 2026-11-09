import json
import os
import tempfile
from pathlib import Path


def load_state(path):
    p = Path(path)
    if not p.exists():
        return {"watermark": None}
    return {"watermark": None, **json.loads(p.read_text())}


def save_state(path, state):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=p.parent, prefix=p.name + ".")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(state, fh, sort_keys=True)
        os.replace(tmp, p)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
