from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

_INVOICES = {1: {"invoice_id": 1, "amount": 120.0}}


def get_store() -> dict[int, dict]:
    return _INVOICES


def get_api_key() -> str:
    return "secret"


def require_api_key(
    x_api_key: str | None = Header(default=None),
    expected: str = Depends(get_api_key),
) -> None:
    if x_api_key != expected:
        raise HTTPException(status_code=401, detail="bad api key")


@app.get("/invoices/{invoice_id}", dependencies=[Depends(require_api_key)])
def get_invoice(invoice_id: int, store: dict = Depends(get_store)) -> dict:
    if invoice_id not in store:
        raise HTTPException(status_code=404, detail="invoice not found")
    return store[invoice_id]
