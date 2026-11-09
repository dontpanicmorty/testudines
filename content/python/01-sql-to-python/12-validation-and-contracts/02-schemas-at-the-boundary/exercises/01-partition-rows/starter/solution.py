from pydantic import BaseModel


def partition(rows: list[dict], model: type[BaseModel]) -> tuple[list[BaseModel], list[dict]]:
    """Split rows into validated models and reject records."""
    raise NotImplementedError
