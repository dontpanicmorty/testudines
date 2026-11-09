from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path


class ConfigError(Exception):
    """Raised when settings are missing or invalid."""


@dataclass(frozen=True)
class JobConfig:
    input_path: Path
    output_dir: Path
    max_error_rate: float = 0.1
    log_level: str = "INFO"


def load_config(env: Mapping[str, str]) -> JobConfig:
    # TODO: read JOB_INPUT, JOB_OUTPUT_DIR, JOB_MAX_ERROR_RATE, JOB_LOG_LEVEL
    raise NotImplementedError
