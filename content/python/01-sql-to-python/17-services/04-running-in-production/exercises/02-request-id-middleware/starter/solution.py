from fastapi import FastAPI


def add_request_id(app: FastAPI) -> None:
    """Install the request-id + access-log middleware on app."""
