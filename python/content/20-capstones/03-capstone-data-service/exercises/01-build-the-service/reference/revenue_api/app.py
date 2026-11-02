"""Routes."""
import json
from datetime import date
from typing import Annotated

import duckdb
from fastapi import Depends, FastAPI, Header, HTTPException, Query, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .db import connect, fetch_all, get_conn
from .errors import install_error_handlers
from .models import (Customer, CustomerPage, DayDetail, NewCustomer, RegionRevenue, RevenuePage)
from .settings import Settings, get_settings, get_today

Conn = duckdb.DuckDBPyConnection


def paging(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int | None, Query(ge=1)] = None,
    settings: Settings = Depends(get_settings),
) -> tuple[int, int]:
    size = settings.default_page_size if page_size is None else page_size
    if size > settings.max_page_size:
        raise RequestValidationError(
            [{"type": "less_than_equal", "loc": ("query", "page_size"),
              "msg": f"page_size must be <= {settings.max_page_size}", "input": page_size}]
        )
    return page, size


def _page_meta(page: int, size: int, total: int) -> dict:
    return {"page": page, "page_size": size, "total": total, "has_next": page * size < total}


def create_app() -> FastAPI:
    app = FastAPI(title="Revenue API")
    install_error_handlers(app)

    @app.get("/health")
    def health(response: Response, settings: Settings = Depends(get_settings)) -> dict:
        try:
            conn = connect(settings.db_path)
            try:
                conn.execute("select 1")
            finally:
                conn.close()
            return {"status": "ok", "database": "up"}
        except duckdb.Error:
            response.status_code = 503
            return {"status": "degraded", "database": "down"}

    @app.get("/revenue/daily", response_model=RevenuePage)
    def revenue_daily(
        start: date | None = None,
        end: date | None = None,
        region: str | None = None,
        pg: tuple[int, int] = Depends(paging),
        conn: Conn = Depends(get_conn),
    ):
        if start and end and start > end:
            raise RequestValidationError(
                [{"type": "value_error", "loc": ("query", "start"), "msg": "start must be <= end", "input": str(start)}]
            )
        page, size = pg
        clauses, params = [], []
        if start:
            clauses.append("day >= ?"); params.append(start)
        if end:
            clauses.append("day <= ?"); params.append(end)
        if region:
            clauses.append("region = ?"); params.append(region)
        where = f" where {' and '.join(clauses)}" if clauses else ""
        total = conn.execute(f"select count(*) from daily_revenue{where}", params).fetchone()[0]
        items = fetch_all(
            conn,
            f"select day, region, orders, round(revenue, 2) as revenue from daily_revenue{where} "
            "order by day, region limit ? offset ?",
            [*params, size, (page - 1) * size],
        )
        return {**_page_meta(page, size, total), "items": items}

    @app.get("/revenue/daily/{day}", response_model=DayDetail)
    def revenue_day(day: date, conn: Conn = Depends(get_conn)):
        regions = fetch_all(
            conn,
            "select region, orders, round(revenue, 2) as revenue from daily_revenue where day = ? order by region",
            [day],
        )
        if not regions:
            raise HTTPException(status_code=404, detail=f"no revenue for {day}")
        return {
            "day": day,
            "orders": sum(r["orders"] for r in regions),
            "revenue": round(sum(r["revenue"] for r in regions), 2),
            "regions": [RegionRevenue(**r) for r in regions],
        }

    customer_cols = "customer_id, first_name, last_name, region, plan, signup_date"

    @app.get("/customers", response_model=CustomerPage)
    def list_customers(
        region: str | None = None,
        plan: str | None = None,
        pg: tuple[int, int] = Depends(paging),
        conn: Conn = Depends(get_conn),
    ):
        page, size = pg
        clauses, params = [], []
        if region:
            clauses.append("region = ?"); params.append(region)
        if plan:
            clauses.append("plan = ?"); params.append(plan)
        where = f" where {' and '.join(clauses)}" if clauses else ""
        total = conn.execute(f"select count(*) from customers{where}", params).fetchone()[0]
        items = fetch_all(
            conn,
            f"select {customer_cols} from customers{where} order by customer_id limit ? offset ?",
            [*params, size, (page - 1) * size],
        )
        return {**_page_meta(page, size, total), "items": items}

    @app.get("/customers/{customer_id}", response_model=Customer)
    def get_customer(customer_id: int, conn: Conn = Depends(get_conn)):
        rows = fetch_all(conn, f"select {customer_cols} from customers where customer_id = ?", [customer_id])
        if not rows:
            raise HTTPException(status_code=404, detail=f"customer {customer_id} not found")
        return rows[0]

    @app.post("/customers", status_code=201, response_model=Customer)
    def create_customer(
        body: NewCustomer,
        idempotency_key: str = Header(min_length=1),
        today: date = Depends(get_today),
        conn: Conn = Depends(get_conn),
    ):
        email = body.email.strip().lower()
        fingerprint = json.dumps({**body.model_dump(), "email": email}, sort_keys=True)
        conn.execute(
            "create table if not exists idempotency_keys "
            "(key varchar primary key, fingerprint varchar, response varchar)"
        )
        seen = conn.execute(
            "select fingerprint, response from idempotency_keys where key = ?", [idempotency_key]
        ).fetchone()
        if seen:
            if seen[0] != fingerprint:
                raise HTTPException(status_code=409, detail="idempotency key reused with a different body")
            return JSONResponse(json.loads(seen[1]), status_code=201)
        if conn.execute("select count(*) from customers where lower(email) = ?", [email]).fetchone()[0]:
            raise HTTPException(status_code=409, detail="email already exists")
        conn.execute("begin")
        try:
            new_id = conn.execute("select coalesce(max(customer_id), 0) + 1 from customers").fetchone()[0]
            conn.execute(
                "insert into customers (customer_id, first_name, last_name, email, region, plan, signup_date) "
                "values (?, ?, ?, ?, ?, ?, ?)",
                [new_id, body.first_name, body.last_name, email, body.region, body.plan, today],
            )
            created = Customer(customer_id=new_id, first_name=body.first_name, last_name=body.last_name,
                               region=body.region, plan=body.plan, signup_date=today)
            conn.execute(
                "insert into idempotency_keys values (?, ?, ?)",
                [idempotency_key, fingerprint, created.model_dump_json()],
            )
            conn.execute("commit")
        except Exception:
            conn.execute("rollback")
            raise
        return created

    return app
