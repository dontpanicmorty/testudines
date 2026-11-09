from collections import Counter


def error_report(rejects: list[dict], total_rows: int) -> dict:
    """Summarise reject records. See prompt.md."""
    errors = Counter()
    rows = Counter()
    for reject in rejects:
        fields = [e["field"] for e in reject["errors"]]
        errors.update(fields)
        rows.update(set(fields))
    by_field = [
        {"field": f, "error_count": n, "rows_affected": rows[f]}
        for f, n in sorted(errors.items(), key=lambda kv: (-kv[1], kv[0]))
    ]
    return {
        "rejected": len(rejects),
        "reject_rate": round(len(rejects) / total_rows, 4) if total_rows else 0.0,
        "by_field": by_field,
        "sample_indexes": [r["index"] for r in rejects[:3]],
    }
