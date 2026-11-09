"""One error envelope for every failure."""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

_CODES = {404: "not_found", 409: "conflict"}


def envelope(status: int, code: str, message: str, **extra) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message, **extra}})


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_error(request: Request, exc: StarletteHTTPException):
        return envelope(exc.status_code, _CODES.get(exc.status_code, "http_error"), str(exc.detail))

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        fields = [".".join(str(p) for p in e["loc"]) for e in exc.errors()]
        return envelope(422, "validation_error", "invalid request", fields=fields)

    @app.exception_handler(Exception)
    async def unexpected(request: Request, exc: Exception):
        return envelope(500, "internal_error", "internal server error")
