def locate(conn, name, geocoder):
    row = conn.execute("SELECT lat, lon FROM place WHERE name = ?", (name,)).fetchone()
    if row is not None:
        return (row[0], row[1])
    lat, lon = geocoder(name)
    conn.execute("INSERT INTO place (name, lat, lon) VALUES (?, ?, ?)", (name, lat, lon))
    conn.commit()
    return (lat, lon)
