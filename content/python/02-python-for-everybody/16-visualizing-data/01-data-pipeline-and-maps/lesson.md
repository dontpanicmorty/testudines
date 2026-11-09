+++
id = "everybody.visualizing-data.data-pipeline-and-maps"
title = "From raw data to a map"
minutes = 30
+++

# From raw data to a map

Data rarely arrives ready to draw. Between a raw pile of facts and a picture, there is usually a chain of steps. Seeing that chain clearly will help you design every project in this chapter.

## The pipeline

1. **Gather**: collect the raw data (read files, call an API, scrape pages).
2. **Clean**: fix or drop bad values, make spellings consistent.
3. **Store**: keep the cleaned data in a database or file so you do not repeat work.
4. **Visualize**: turn the stored data into something a person can look at.

Each step reads the output of the one before. That makes each step easy to test on its own, and lets you rerun only the step you changed.

## A map project, in outline

Suppose you have a list of towns where a club holds meetings, typed by hand:

```
Larkfield
Oakby
Thistle End
```

To draw them on a map you need coordinates: **latitude** (north-south) and **longitude** (east-west). Turning a place name into coordinates is called **geocoding**, and real projects usually ask a geocoding web service, which takes a name in a query string and answers with JSON that includes coordinates.

Such services limit how many questions you may ask, as you saw in the web services chapter. And if you rerun your program, you would ask about the same towns again. The standard answer is a **cache**: store each answer the first time, and look there first.

We cannot reach the internet in this course, so we will make up coordinates for made-up towns and pass in a function that plays the part of the service. The shape of the code is the same as for the real thing.

## Cleaning first

Hand-typed or downloaded rows contain mistakes. A row might have a latitude of `"n/a"`, or a latitude of 250, which cannot exist (valid latitudes run from -90 to 90 and longitudes from -180 to 180).

```python
def clean_row(line):
    parts = line.split(",")
    if len(parts) != 3:
        return None
    name, lat_text, lon_text = (p.strip() for p in parts)
    try:
        lat, lon = float(lat_text), float(lon_text)
    except ValueError:
        return None
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return None
    return {"name": name, "lat": lat, "lon": lon}
```

Returning `None` for bad rows lets the caller decide to skip them. Cleaning code should never crash on the odd bad row.

## A cache in SQLite

```python
import sqlite3

conn = sqlite3.connect("places.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS place (
        name TEXT PRIMARY KEY,
        lat  REAL,
        lon  REAL
    )
""")

def locate(conn, name, geocoder):
    row = conn.execute("SELECT lat, lon FROM place WHERE name = ?", (name,)).fetchone()
    if row is not None:
        return row                       # cache hit: no lookup needed
    lat, lon = geocoder(name)            # cache miss: ask the service
    conn.execute("INSERT INTO place (name, lat, lon) VALUES (?, ?, ?)", (name, lat, lon))
    conn.commit()
    return (lat, lon)
```

The first call for a town runs the geocoder and stores the answer. Every later call is answered from the table instantly. If the program is interrupted halfway, you lose nothing, because each answer was committed.

## Writing data for a web page

A web page cannot read your SQLite file. The common bridge is to write the points into a small **JavaScript file** (or a JSON file) that the page loads. The page's own code then draws a marker for each point using a mapping library.

```python
import json

points = [["Larkfield", 51.2, -1.4], ["Oakby", 51.5, -1.1]]
with open("points.js", "w", encoding="utf-8") as f:
    f.write("var points = " + json.dumps(points) + ";\n")
```

The file will contain:

```
var points = [["Larkfield", 51.2, -1.4], ["Oakby", 51.5, -1.1]];
```

A page includes it with `<script src="points.js"></script>`, and then JavaScript can use the variable `points`. Using `json.dumps` matters: it escapes quotes and special characters properly, so a name like `O'Neil "Quay"` cannot break the file.

In a real project, the page would also load a free mapping library and a map-tile service from the web to show the background. Your Python code stays the same, because its only job is to produce the data file.

## Debugging tip

Check each stage before moving on. Print how many rows survived cleaning. Count rows in the cache table. Open the output file in a text editor. When the final picture looks wrong, you can then tell quickly which stage went wrong.

## Common mistakes

- Skipping the cleaning step and finding out about bad coordinates only when the map looks odd.
- Building JavaScript text by gluing strings, which breaks on names with quotes.
- Forgetting to commit cache writes, so every run starts from scratch.
- Swapping latitude and longitude. Latitude comes first.
