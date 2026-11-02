import csv
from pathlib import Path


def split_by_region(src, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    groups = {}
    with open(src, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            groups.setdefault(row["region"], []).append(row)
    counts = {}
    for region, rows in groups.items():
        with open(out_dir / f"{region}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)
        counts[region] = len(rows)
    return counts
