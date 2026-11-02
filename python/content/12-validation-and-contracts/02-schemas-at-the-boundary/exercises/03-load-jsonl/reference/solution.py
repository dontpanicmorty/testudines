import json

from pydantic import BaseModel, ValidationError


class TooManyRejects(Exception):
    pass


def load_events(lines, model: type[BaseModel], max_reject_rate: float = 0.25):
    """Parse JSONL lines into models, quarantining bad ones."""
    valid: list[BaseModel] = []
    rejects: list[dict] = []
    for line_no, line in enumerate(lines, start=1):
        text = line.strip()
        if not text:
            continue
        try:
            obj = json.loads(text)
        except json.JSONDecodeError as exc:
            rejects.append({"line_no": line_no, "line": line, "reason": f"invalid json: {exc.msg}"})
            continue
        if not isinstance(obj, dict):
            rejects.append({"line_no": line_no, "line": line, "reason": "not an object"})
            continue
        try:
            valid.append(model.model_validate(obj))
        except ValidationError as exc:
            fields = sorted({".".join(str(p) for p in e["loc"]) or "__row__" for e in exc.errors()})
            rejects.append({"line_no": line_no, "line": line, "reason": "invalid fields: " + ", ".join(fields)})
    total = len(valid) + len(rejects)
    if total and len(rejects) / total > max_reject_rate:
        raise TooManyRejects(f"{len(rejects)}/{total} lines rejected")
    return valid, rejects
