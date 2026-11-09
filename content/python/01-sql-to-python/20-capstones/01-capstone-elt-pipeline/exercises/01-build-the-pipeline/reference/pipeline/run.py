"""Orchestration: extract, validate, transform, load."""
import csv
import logging
from pathlib import Path

from . import load, schema, transform

log = logging.getLogger("pipeline")


def read_csv_rows(path: Path) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def run_pipeline(data_dir: str | Path, db_path: str | Path, incremental: bool = False) -> dict:
    data_dir = Path(data_dir)
    raw_orders = read_csv_rows(data_dir / "orders.csv")
    raw_items = read_csv_rows(data_dir / "order_items.csv")
    raw_customers = read_csv_rows(data_dir / "customers.csv")

    orders, bad_orders = schema.validate_orders(raw_orders)
    items, bad_items = schema.validate_items(raw_items)
    customers, bad_customers = schema.validate_customers(raw_customers)
    quarantined = bad_orders + bad_items + bad_customers
    if quarantined:
        log.warning("quarantined %d bad rows", len(quarantined))

    conn = load.connect(db_path)
    try:
        watermark = load.get_watermark(conn) if incremental else None
        if watermark:
            orders = [o for o in orders if o["placed_at"][:10] >= watermark]
            log.info("incremental run from %s", watermark)
        rows = transform.daily_revenue(orders, items, customers)
        load.save_quarantine(conn, quarantined)
        replace_all = not incremental
        loaded = load.load_daily_revenue(conn, rows, replace_all=replace_all)
        if rows:
            load.set_watermark(conn, max(r["day"] for r in rows))
        new_watermark = load.get_watermark(conn)
    finally:
        conn.close()

    stats = {
        "orders_read": len(raw_orders),
        "orders_valid": len(orders),
        "orders_quarantined": len(bad_orders),
        "items_quarantined": len(bad_items),
        "customers_quarantined": len(bad_customers),
        "rows_loaded": loaded,
        "watermark": new_watermark,
    }
    log.info("loaded %d daily revenue rows", loaded)
    return stats
