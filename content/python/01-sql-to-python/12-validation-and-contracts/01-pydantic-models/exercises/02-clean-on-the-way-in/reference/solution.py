from typing import Literal

from pydantic import BaseModel, field_validator


class CleanInvoice(BaseModel):
    invoice_id: str
    customer: str
    amount: float | None = None
    status: Literal["paid", "open", "overdue", "unknown"] = "unknown"

    @field_validator("invoice_id", mode="before")
    @classmethod
    def _id(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("customer", mode="before")
    @classmethod
    def _customer(cls, value):
        return value.strip().title() if isinstance(value, str) else value

    @field_validator("amount", mode="before")
    @classmethod
    def _amount(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            text = value.replace("$", "").replace(",", "").strip()
            if text == "" or text.upper() == "N/A":
                return None
            return text
        return value

    @field_validator("status", mode="before")
    @classmethod
    def _status(cls, value):
        if value is None:
            return "unknown"
        if isinstance(value, str):
            text = value.strip().lower()
            return text or "unknown"
        return value


def parse_clean(row: dict) -> CleanInvoice:
    return CleanInvoice.model_validate(row)
