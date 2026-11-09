from pydantic import BaseModel, ValidationError


def partition(rows: list[dict], model: type[BaseModel]) -> tuple[list[BaseModel], list[dict]]:
    """Split rows into validated models and reject records."""
    valid: list[BaseModel] = []
    rejects: list[dict] = []
    for index, row in enumerate(rows):
        try:
            valid.append(model.model_validate(row))
        except ValidationError as exc:
            errors = [
                {"field": ".".join(str(p) for p in e["loc"]) or "__row__", "message": e["msg"]}
                for e in exc.errors()
            ]
            rejects.append({"index": index, "row": row, "errors": errors})
    return valid, rejects
