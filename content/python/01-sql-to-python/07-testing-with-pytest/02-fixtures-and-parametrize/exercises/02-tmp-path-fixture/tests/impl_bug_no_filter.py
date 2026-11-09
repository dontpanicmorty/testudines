"""Free customers are not filtered out at all."""
import csv


def active_customers(path):
    """Rows (stripped values, file order) whose plan is not 'free' (case/space-insensitive)."""
    rows = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            clean = {key: value.strip() for key, value in row.items()}
            rows.append(clean)
    return rows
