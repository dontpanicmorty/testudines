`conn` has the table `place(name TEXT PRIMARY KEY, lat REAL, lon REAL)`. Write `write_points_js(conn, path)` that writes a file at `path` (a string or `Path`) containing a single line of JavaScript:

```
var points = [["Larkfield", 51.2, -1.4], ["Oakby", 51.5, -1.1]];
```

Each point is `[name, lat, lon]`, and points are ordered by name. The line ends with `;` and a newline. With no rows, the array is `[]`. Return the number of points written.
