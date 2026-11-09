from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class PaymentIn(BaseModel):
    customer_id: int
    amount: float = Field(gt=0)


def create_app() -> FastAPI:
    app = FastAPI()
    payments: list[dict] = []
    seen: dict[str, tuple[tuple, int, dict]] = {}

    @app.post("/payments", status_code=201)
    def create_payment(body: PaymentIn, idempotency_key: str = Header(min_length=1)):
        fingerprint = (body.customer_id, body.amount)
        if idempotency_key in seen:
            fp, status, stored = seen[idempotency_key]
            if fp != fingerprint:
                raise HTTPException(status_code=409, detail="idempotency key reused with a different body")
            return JSONResponse(stored, status_code=status)
        payment = {"payment_id": len(payments) + 1, "customer_id": body.customer_id, "amount": body.amount}
        payments.append(payment)
        seen[idempotency_key] = (fingerprint, 201, payment)
        return payment

    @app.get("/payments")
    def list_payments() -> dict:
        return {"items": payments}

    return app
