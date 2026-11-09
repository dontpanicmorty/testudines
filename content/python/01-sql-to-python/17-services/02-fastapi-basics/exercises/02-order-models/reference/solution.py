from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class ItemIn(BaseModel):
    sku: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)


class OrderIn(BaseModel):
    customer_id: int
    items: list[ItemIn] = Field(min_length=1)


class OrderOut(BaseModel):
    order_id: int
    customer_id: int
    total: float


def create_app() -> FastAPI:
    app = FastAPI()
    orders: dict[int, OrderOut] = {}

    @app.post("/orders", status_code=201, response_model=OrderOut)
    def create_order(order: OrderIn) -> OrderOut:
        total = round(sum(i.quantity * i.unit_price for i in order.items), 2)
        order_id = len(orders) + 1
        out = OrderOut(order_id=order_id, customer_id=order.customer_id, total=total)
        orders[order_id] = out
        return out

    @app.get("/orders/{order_id}", response_model=OrderOut)
    def get_order(order_id: int) -> OrderOut:
        if order_id not in orders:
            raise HTTPException(status_code=404, detail="order not found")
        return orders[order_id]

    return app
