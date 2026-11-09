import json


def write_points_js(conn, path):
    rows = conn.execute("SELECT name, lat, lon FROM place ORDER BY name").fetchall()
    points = [[name, lat, lon] for name, lat, lon in rows]
    with open(path, "w", encoding="utf-8") as f:
        f.write("var points = " + json.dumps(points) + ";\n")
    return len(points)
