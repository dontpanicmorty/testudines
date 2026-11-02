from fastapi import FastAPI


def create_app(db_path: str) -> FastAPI:
    app = FastAPI()
    # TODO: get_db dependency, GET /orders, GET /health
    return app
