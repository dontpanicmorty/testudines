from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()
    # TODO: POST /payments with Idempotency-Key, GET /payments
    return app
