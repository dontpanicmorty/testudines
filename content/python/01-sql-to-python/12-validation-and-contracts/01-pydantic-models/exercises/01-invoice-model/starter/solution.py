from pydantic import BaseModel


class Invoice(BaseModel):
    pass


def parse_invoice(row: dict) -> Invoice:
    raise NotImplementedError
