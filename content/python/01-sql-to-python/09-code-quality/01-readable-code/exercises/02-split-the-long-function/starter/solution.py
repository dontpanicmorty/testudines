"""Invoice report."""


def process(t):
    out = []
    d = {}
    lines = t.strip().splitlines()
    h = lines[0].split(",")
    for l in lines[1:]:
        if l.strip() == "":
            continue
        p = l.split(",")
        r = dict(zip(h, p))
        s = r["status"].strip().lower()
        if s == "paid":
            n = r["customer"].strip()
            a = float(r["amount"].strip().replace("$", ""))
            if n in d:
                d[n] = d[n] + a
            else:
                d[n] = a
    items = sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))
    for k, v in items:
        out.append(f"{k}: {v:.2f}")
    tot = 0
    for k, v in items:
        tot += v
    out.append(f"TOTAL: {tot:.2f}")
    return "\n".join(out)
