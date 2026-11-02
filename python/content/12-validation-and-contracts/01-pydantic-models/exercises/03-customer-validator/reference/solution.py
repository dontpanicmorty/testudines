from datetime import date

from pydantic import BaseModel, field_validator


class Customer(BaseModel):
    customer_id: int
    email: str
    signup_date: date

    @field_validator("email")
    @classmethod
    def normalise_email(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value:
            raise ValueError("email must contain @")
        return value
