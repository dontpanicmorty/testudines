Write `create_app()` returning a FastAPI app with `POST /payments` and `GET /payments`.

`POST /payments` body: `{"customer_id": int, "amount": number > 0}`, header `Idempotency-Key` (required; missing gives `422`).

- First time a key is seen: create the payment, respond `201` with `{"payment_id": N, "customer_id": ..., "amount": ...}` (ids start at 1).
- Same key and **identical** body again: respond with the **same status and body** as the first time, and create nothing.
- Same key but a **different** body: respond `409` and create nothing.
- An invalid body gives `422` and must **not** reserve the key: sending a corrected body with that key afterwards creates the payment normally.

`GET /payments` returns `{"items": [...all payments in creation order...]}`.

```python
c = TestClient(create_app())
h = {"Idempotency-Key": "k1"}
c.post("/payments", json={"customer_id": 1, "amount": 25}, headers=h)   # 201
c.post("/payments", json={"customer_id": 1, "amount": 25}, headers=h)   # 201, same body, no new row
c.post("/payments", json={"customer_id": 1, "amount": 99}, headers=h)   # 409
```
