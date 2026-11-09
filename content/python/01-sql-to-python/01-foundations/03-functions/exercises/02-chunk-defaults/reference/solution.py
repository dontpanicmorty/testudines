def build_query(table, schema="analytics", limit=None, **filters):
    sql = f"SELECT * FROM {schema}.{table}"
    if filters:
        conds = [f"{col} = '{filters[col]}'" for col in sorted(filters)]
        sql += " WHERE " + " AND ".join(conds)
    if limit is not None:
        sql += f" LIMIT {limit}"
    return sql
