def clean_places(lines):
    result = []
    for line in lines:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 3:
            continue
        name, lat_text, lon_text = parts
        try:
            lat, lon = float(lat_text), float(lon_text)
        except ValueError:
            continue
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            result.append({"name": name, "lat": lat, "lon": lon})
    return result
