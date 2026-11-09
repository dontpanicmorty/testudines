from pathlib import Path


def write_daily_report(out_dir, day, lines):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{day}.txt"
    with path.open("w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    return path
