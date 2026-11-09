from typing import Literal

from pydantic import BaseModel, Field


class Invoice(BaseModel):
    invoice_id: str
    customer: str
    amount: float = Field(ge=0)
    status: Literal["paid", "open", "overdue"]


def parse_invoice(row: dict) -> Invoice:
    return Invoice.model_validate(row)
