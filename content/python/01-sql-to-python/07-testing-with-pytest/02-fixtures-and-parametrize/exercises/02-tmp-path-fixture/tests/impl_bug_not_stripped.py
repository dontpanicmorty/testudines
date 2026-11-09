"""Values are returned without being stripped."""
import csv


def active_customers(path):
    """Rows (stripped values, file order) whose plan is not 'free' (case/space-insensitive)."""
    rows = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            if row["plan"].strip().lower() != "free":
                rows.append(row)
    return rows
