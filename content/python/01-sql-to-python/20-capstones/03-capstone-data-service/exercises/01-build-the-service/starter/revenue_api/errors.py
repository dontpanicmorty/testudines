"""One error envelope for every failure."""
from fastapi import FastAPI


def install_error_handlers(app: FastAPI) -> None:
    """Register handlers so every error body is {"error": {"code", "message", ...}}.

    http errors (including unknown routes): code not_found (404), conflict (409), else http_error
    request validation: 422, code validation_error, message "invalid request", extra key
        "fields": dotted locations such as "query.page_size" or "path.customer_id"
    anything else: 500, code internal_error, message "internal server error" (never the exception text)
    """
    raise NotImplementedError
