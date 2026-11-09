ENVIRONMENTS = {
    "dev": {"database": "ANALYTICS_DEV", "warehouse": "DEV_WH", "role": "LOADER_DEV"},
    "prod": {"database": "ANALYTICS", "warehouse": "PROD_WH", "role": "LOADER"},
}


def environment_params(name: str, *, allow_prod: bool = False) -> dict:
    return ENVIRONMENTS[name]
