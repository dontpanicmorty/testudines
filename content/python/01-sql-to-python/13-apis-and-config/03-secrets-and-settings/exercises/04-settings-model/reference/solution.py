from collections.abc import Mapping

from pydantic import BaseModel, SecretStr, ValidationError


class ConfigError(Exception):
    pass


class Settings(BaseModel, frozen=True):
    api_url: str
    api_token: SecretStr
    timeout_s: float = 10.0
    batch_size: int = 500
    debug: bool = False


def load_settings(env: Mapping[str, str]) -> Settings:
    data = {}
    for name in Settings.model_fields:
        key = f"APP_{name.upper()}"
        if key in env:
            data[name] = env[key]
    try:
        return Settings(**data)
    except ValidationError as exc:
        bad = sorted({f"APP_{str(e['loc'][0]).upper()}" for e in exc.errors()})
        raise ConfigError("invalid or missing settings: " + ", ".join(bad)) from None
