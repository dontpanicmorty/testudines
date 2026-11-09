from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

_INVOICES = {1: {"invoice_id": 1, "amount": 120.0}}


def get_store() -> dict[int, dict]:
    return _INVOICES


def get_api_key() -> str:
    return "secret"


@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int, x_api_key: str | None = Header(default=None)) -> dict:
    if x_api_key != get_api_key():
        raise HTTPException(status_code=401, detail="bad api key")
    store = get_store()
    if invoice_id not in store:
        raise HTTPException(status_code=404, detail="invoice not found")
    return store[invoice_id]
