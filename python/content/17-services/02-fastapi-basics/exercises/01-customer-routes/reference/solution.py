from typing import Annotated

from fastapi import FastAPI, HTTPException, Query


def create_app(customers: list[dict]) -> FastAPI:
    app = FastAPI()
    by_id = {c["customer_id"]: c for c in customers}

    @app.get("/customers/{customer_id}")
    def get_customer(customer_id: int) -> dict:
        if customer_id not in by_id:
            raise HTTPException(status_code=404, detail=f"customer {customer_id} not found")
        return by_id[customer_id]

    @app.get("/customers")
    def list_customers(
        region: str | None = None,
        limit: Annotated[int, Query(ge=1, le=100)] = 10,
        offset: Annotated[int, Query(ge=0)] = 0,
    ) -> dict:
        rows = [c for c in customers if region is None or c["region"] == region]
        return {"items": rows[offset : offset + limit], "total": len(rows)}

    return app
