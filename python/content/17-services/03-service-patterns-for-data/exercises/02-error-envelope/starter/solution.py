from fastapi import FastAPI


def install_error_handlers(app: FastAPI) -> None:
    """Register handlers so every error uses the {"error": {...}} envelope."""
