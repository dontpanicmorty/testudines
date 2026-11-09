import sqlite3
from typing import Annotated

from fastapi import Depends, FastAPI, Query, Response


def create_app(db_path: str) -> FastAPI:
    app = FastAPI()

    def get_db():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    @app.get("/orders")
    def list_orders(
        page: Annotated[int, Query(ge=1)] = 1,
        page_size: Annotated[int, Query(ge=1, le=50)] = 10,
        status: str | None = None,
        db: sqlite3.Connection = Depends(get_db),
    ) -> dict:
        where, params = "", []
        if status is not None:
            where, params = " where status = ?", [status]
        total = db.execute(f"select count(*) from orders{where}", params).fetchone()[0]
        rows = db.execute(
            f"select order_id, customer_id, status from orders{where} order by order_id limit ? offset ?",
            [*params, page_size, (page - 1) * page_size],
        ).fetchall()
        return {
            "items": [dict(r) for r in rows],
            "page": page,
            "page_size": page_size,
            "total": total,
            "has_next": page * page_size < total,
        }

    @app.get("/health")
    def health(response: Response) -> dict:
        try:
            conn = sqlite3.connect(db_path)
            try:
                conn.execute("select 1")
            finally:
                conn.close()
            return {"status": "ok"}
        except sqlite3.Error:
            response.status_code = 503
            return {"status": "down"}

    return app
