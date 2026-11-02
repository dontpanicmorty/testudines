import duckdb


def run_models(con: duckdb.DuckDBPyConnection, models: dict[str, str]) -> list[str]:
    """Render ref() templates, order by dependency, build each as a table."""
    raise NotImplementedError
