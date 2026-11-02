"""Generates the bundled practice datasets. Deterministic, stdlib only, all synthetic."""
import csv
import json
import random
from datetime import date, datetime, timedelta
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "datasets"
OUT.mkdir(exist_ok=True)
R = random.Random(20261102)

FIRST = "Ada Grace Alan Linus Margaret Dennis Barbara Ken Radia Guido Donald Frances Tim Hedy Katherine Claude Edsger Joan Vint Shafi".split()
LAST = "Lovelace Hopper Turing Torvalds Hamilton Ritchie Liskov Thompson Perlman Rossum Knuth Allen Berners Lamarr Johnson Shannon Dijkstra Clarke Cerf Goldwasser".split()
REGIONS = ["northeast", "southeast", "midwest", "west", "southwest"]
PLANS = ["free", "pro", "team", "enterprise"]

# customers
customers = []
for i in range(1, 201):
    f, l = R.choice(FIRST), R.choice(LAST)
    customers.append({"customer_id": i, "first_name": f, "last_name": l,
                      "email": f"{f}.{l}{i}@example.com".lower(), "region": R.choice(REGIONS),
                      "plan": R.choices(PLANS, [50, 30, 15, 5])[0],
                      "signup_date": (date(2024, 1, 1) + timedelta(days=R.randint(0, 600))).isoformat()})
with open(OUT / "customers.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(customers[0])); w.writeheader(); w.writerows(customers)

# products
products = [("P%03d" % i, n, c, round(R.uniform(4, 400), 2)) for i, (n, c) in enumerate([
    ("Notebook", "office"), ("Desk Lamp", "office"), ("Standing Desk", "furniture"), ("Chair", "furniture"),
    ("Keyboard", "electronics"), ("Mouse", "electronics"), ("Monitor", "electronics"), ("Webcam", "electronics"),
    ("Headphones", "electronics"), ("Whiteboard", "office"), ("Bookshelf", "furniture"), ("Cable Kit", "electronics")], 1)]
with open(OUT / "products.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["product_id", "name", "category", "unit_price"]); w.writerows(products)

# orders + order_items
orders, items = [], []
oid = 1000
for _ in range(1500):
    oid += 1
    c = R.choice(customers)
    placed = datetime(2025, 1, 1) + timedelta(minutes=R.randint(0, 60 * 24 * 420))
    status = R.choices(["completed", "shipped", "cancelled", "refunded"], [70, 15, 10, 5])[0]
    orders.append({"order_id": oid, "customer_id": c["customer_id"], "placed_at": placed.isoformat(sep=" "), "status": status})
    for _ in range(R.randint(1, 4)):
        p = R.choice(products)
        items.append({"order_id": oid, "product_id": p[0], "quantity": R.randint(1, 5), "unit_price": p[3]})
for name, rows in (("orders", orders), ("order_items", items)):
    with open(OUT / f"{name}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

# events (jsonl, nested, a few malformed lines on purpose)
with open(OUT / "events.jsonl", "w") as fh:
    for i in range(2000):
        c = R.choice(customers)
        ts = datetime(2025, 6, 1) + timedelta(seconds=R.randint(0, 86400 * 30))
        ev = {"event_id": f"e{i:05d}", "ts": ts.isoformat(), "user": {"id": c["customer_id"], "plan": c["plan"]},
              "type": R.choices(["page_view", "click", "purchase", "login"], [60, 25, 5, 10])[0],
              "props": {"path": R.choice(["/", "/pricing", "/docs", "/app"]), "ms": R.randint(5, 900)}}
        if R.random() < 0.15:
            del ev["props"]["ms"]
        fh.write(json.dumps(ev) + "\n")
        if i in (400, 1200, 1700):
            fh.write("{this line is corrupt\n")

# messy export (inconsistent casing, whitespace, dates, missing values, duplicates, currency strings)
messy = [["Invoice #", "Customer Name ", "AMOUNT", "Invoice Date", "Status"]]
for i in range(1, 121):
    d = date(2025, 1, 1) + timedelta(days=R.randint(0, 300))
    fmt = R.choice(["%Y-%m-%d", "%m/%d/%Y", "%d %b %Y"])
    amt = R.choice([f"${R.uniform(50, 5000):,.2f}", f"{R.uniform(50, 5000):.2f}", "", "N/A"])
    name = R.choice(FIRST) + " " + R.choice(LAST)
    name = R.choice([name, name.upper(), "  " + name.lower() + " "])
    messy.append([f"INV-{i:04d}", name, amt, d.strftime(fmt), R.choice(["Paid", "paid", "PAID ", "Open", "overdue", ""])])
messy += [messy[5], messy[17], messy[40]]  # exact duplicate rows
with open(OUT / "messy_invoices.csv", "w", newline="") as fh:
    csv.writer(fh).writerows(messy)

# dbt-style manifest (tiny, hand-shaped like the real artifact so lessons transfer)
nodes = {}
def node(kind, name, deps, tags, mat="view"):
    uid = f"{kind}.shop.{name}"
    nodes[uid] = {"unique_id": uid, "resource_type": kind, "name": name, "package_name": "shop",
                  "path": f"{name}.sql", "tags": tags, "config": {"materialized": mat},
                  "depends_on": {"nodes": deps}, "description": f"The {name} model."}
node("model", "stg_customers", ["source.shop.raw.customers"], ["staging"])
node("model", "stg_orders", ["source.shop.raw.orders"], ["staging"])
node("model", "int_order_totals", ["model.shop.stg_orders"], ["intermediate"], "ephemeral")
node("model", "dim_customers", ["model.shop.stg_customers"], ["marts"], "table")
node("model", "fct_orders", ["model.shop.int_order_totals", "model.shop.dim_customers"], ["marts", "finance"], "incremental")
node("test", "not_null_fct_orders_order_id", ["model.shop.fct_orders"], [])
json.dump({"metadata": {"dbt_version": "1.9.0", "project_name": "shop"}, "nodes": nodes,
           "sources": {"source.shop.raw.customers": {"name": "customers"}, "source.shop.raw.orders": {"name": "orders"}}},
          open(OUT / "manifest_sample.json", "w"), indent=2)

# api-style paginated responses
for page in (1, 2, 3):
    users = [{"id": (page - 1) * 5 + k, "name": f"{R.choice(FIRST)} {R.choice(LAST)}", "active": R.random() > 0.3} for k in range(1, 6)]
    json.dump({"page": page, "total_pages": 3, "results": users, "next": page + 1 if page < 3 else None},
              open(OUT / f"api_users_page{page}.json", "w"), indent=2)
print("wrote", sorted(p.name for p in OUT.iterdir()))
