from collections.abc import Mapping

from pydantic import BaseModel


class ConfigError(Exception):
    pass


class Settings(BaseModel):
    api_url: str
    api_token: str
    timeout_s: float = 10.0
    batch_size: int = 500
    debug: bool = False


def load_settings(env: Mapping[str, str]) -> Settings:
    # TODO: read APP_* variables, raise ConfigError naming every bad one
    raise NotImplementedError
