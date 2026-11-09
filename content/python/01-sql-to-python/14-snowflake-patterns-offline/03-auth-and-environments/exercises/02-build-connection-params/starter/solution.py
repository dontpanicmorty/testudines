import json

ENVIRONMENTS = {
    "dev": {"database": "ANALYTICS_DEV", "warehouse": "DEV_WH", "role": "LOADER_DEV"},
    "prod": {"database": "ANALYTICS", "warehouse": "PROD_WH", "role": "LOADER"},
    "oops": {"database": "ANALYTICS_DEV", "warehouse": "DEV_WH", "role": "AccountAdmin"},
}
FORBIDDEN_ROLES = {"ACCOUNTADMIN", "SECURITYADMIN"}


def environment_params(name: str, *, allow_prod: bool = False) -> dict:
    if name not in ENVIRONMENTS:
        raise ValueError(f"unknown environment {name!r}; choose from {sorted(ENVIRONMENTS)}")
    if name == "prod" and not allow_prod:
        raise PermissionError("prod requires allow_prod=True")
    return dict(ENVIRONMENTS[name])


def build_params(env, secrets, job, run_id, *, allow_prod=False) -> dict:
    # TODO
    raise NotImplementedError
