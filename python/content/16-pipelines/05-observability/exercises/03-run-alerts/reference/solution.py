from datetime import datetime


def evaluate_run(metrics, max_age_hours=24, low=0.5, high=2.0, max_reject_rate=0.05):
    alerts = []
    latest = metrics.get("latest_record")
    if latest is None:
        alerts.append("stale")
    else:
        age = datetime.fromisoformat(metrics["now"]) - datetime.fromisoformat(latest)
        if age.total_seconds() / 3600 > max_age_hours:
            alerts.append("stale")
    prev = metrics.get("previous_rows")
    if prev:
        ratio = metrics["rows_written"] / prev
        if ratio < low:
            alerts.append("volume_drop")
        elif ratio > high:
            alerts.append("volume_spike")
    total = metrics["rows_written"] + metrics["rows_rejected"]
    if total and metrics["rows_rejected"] / total > max_reject_rate:
        alerts.append("rejects")
    return alerts
