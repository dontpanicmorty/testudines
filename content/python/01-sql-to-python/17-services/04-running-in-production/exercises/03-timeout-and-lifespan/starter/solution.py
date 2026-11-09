from typing import Awaitable, Callable

from fastapi import FastAPI


def create_app(fetch: Callable[[], Awaitable[str]], events: list[str], timeout: float) -> FastAPI:
    app = FastAPI()
    # TODO: lifespan, /report with timeout, /health
    return app
