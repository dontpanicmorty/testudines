def unpivot(rows, id_field="product"):
    return [
        {id_field: row[id_field], "month": col, "revenue": float(val)}
        for row in rows
        for col, val in row.items()
        if col != id_field and val not in (None, "")
    ]
