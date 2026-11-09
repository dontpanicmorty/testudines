def tag_batch(rows, tags=None):
    all_tags = list(tags) if tags is not None else []
    all_tags.append("loaded")
    return [{**row, "tags": list(all_tags)} for row in rows]
