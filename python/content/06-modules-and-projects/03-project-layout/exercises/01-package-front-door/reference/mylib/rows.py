def read_rows(text):
    lines = [ln for ln in text.splitlines() if ln.strip()]
    header = lines[0].split(",")
    return [dict(zip(header, ln.split(","))) for ln in lines[1:]]
