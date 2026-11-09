def tag_batch(rows, tags=[]):
    tags.append("loaded")
    out = []
    for row in rows:
        row["tags"] = tags
        out.append(row)
    return out
