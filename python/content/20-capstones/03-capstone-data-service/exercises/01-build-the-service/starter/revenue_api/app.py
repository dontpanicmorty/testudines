"""Routes. Build create_app() following the endpoint table in the prompt."""
from fastapi import FastAPI

from .errors import install_error_handlers


def create_app() -> FastAPI:
    app = FastAPI(title="Revenue API")
    install_error_handlers(app)
    # TODO: /health, /revenue/daily, /revenue/daily/{day}, /customers, /customers/{customer_id}, POST /customers
    return app
