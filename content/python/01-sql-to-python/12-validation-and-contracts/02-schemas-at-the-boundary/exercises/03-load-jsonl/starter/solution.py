from pydantic import BaseModel


class TooManyRejects(Exception):
    pass


def load_events(lines, model: type[BaseModel], max_reject_rate: float = 0.25):
    """Parse JSONL lines into models, quarantining bad ones."""
    raise NotImplementedError
