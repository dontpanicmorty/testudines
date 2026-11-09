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
    params = environment_params(env, allow_prod=allow_prod)
    if params["role"].upper() in FORBIDDEN_ROLES:
        raise ValueError(f"role {params['role']} is not allowed for automated jobs")
    params["account"] = secrets["SF_ACCOUNT"]
    params["user"] = secrets["SF_USER"]
    if "SF_PRIVATE_KEY_PATH" in secrets:
        params["authenticator"] = "snowflake_jwt"
        params["private_key_file"] = secrets["SF_PRIVATE_KEY_PATH"]
    elif "SF_PASSWORD" in secrets:
        params["password"] = secrets["SF_PASSWORD"]
    else:
        raise ValueError("no credentials: set SF_PRIVATE_KEY_PATH or SF_PASSWORD")
    tag = json.dumps({"job": job, "env": env, "run": run_id}, sort_keys=True, separators=(",", ":"))
    params["session_parameters"] = {"QUERY_TAG": tag}
    return params
