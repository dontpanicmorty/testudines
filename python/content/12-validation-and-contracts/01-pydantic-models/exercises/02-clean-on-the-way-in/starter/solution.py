from pydantic import BaseModel


class CleanInvoice(BaseModel):
    pass


def parse_clean(row: dict) -> CleanInvoice:
    raise NotImplementedError
