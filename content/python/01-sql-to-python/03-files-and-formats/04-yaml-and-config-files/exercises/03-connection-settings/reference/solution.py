def connection_params(cfg, env):
    var = cfg["password_env"]
    password = env.get(var)
    if not password:
        raise RuntimeError(f"Missing required environment variable: {var}")
    return {
        "account": cfg["account"],
        "user": cfg["user"],
        "warehouse": cfg["warehouse"],
        "password": password,
    }


def describe(cfg):
    return f"{cfg['account']}/{cfg['user']} on {cfg['warehouse']} (password from {cfg['password_env']})"
