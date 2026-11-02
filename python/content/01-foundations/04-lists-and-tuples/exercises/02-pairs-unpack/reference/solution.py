def split_export(lines):
    header, *body = lines
    columns = [c.strip().lower() for c in header.split(",")]
    rows = [tuple(c.strip() for c in line.split(",")) for line in body if line.strip()]
    return columns, rows
