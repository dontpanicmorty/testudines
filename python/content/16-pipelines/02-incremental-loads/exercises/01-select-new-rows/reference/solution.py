def select_new(rows, watermark):
    new = [r for r in rows if watermark is None or r["updated_at"] > watermark]
    new.sort(key=lambda r: r["updated_at"])
    next_mark = max((r["updated_at"] for r in new), default=watermark)
    return new, next_mark
