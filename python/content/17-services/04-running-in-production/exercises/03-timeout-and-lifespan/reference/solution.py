import asyncio
from contextlib import asynccontextmanager
from typing import Awaitable, Callable

from fastapi import FastAPI, HTTPException


def create_app(fetch: Callable[[], Awaitable[str]], events: list[str], timeout: float) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        events.append("startup")
        yield
        events.append("shutdown")

    app = FastAPI(lifespan=lifespan)

    @app.get("/report")
    async def report() -> dict:
        try:
            value = await asyncio.wait_for(fetch(), timeout=timeout)
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="upstream timed out")
        except Exception:
            raise HTTPException(status_code=502, detail="upstream failed")
        return {"report": value}

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok"}

    return app
