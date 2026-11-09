from datetime import datetime, timedelta


def plan_incremental(source_rows, watermark, lookback_hours):
    if watermark is None:
        considered = list(source_rows)
    else:
        start = (datetime.fromisoformat(watermark) - timedelta(hours=lookback_hours)).isoformat()
        considered = [r for r in source_rows if r["updated_at"] >= start]
    latest = {}
    for r in sorted(considered, key=lambda r: r["updated_at"]):
        latest[r["id"]] = r
    return sorted(latest.values(), key=lambda r: r["id"])
