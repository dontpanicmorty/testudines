from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR"}


class ConfigError(Exception):
    """Raised when settings are missing or invalid."""


@dataclass(frozen=True)
class JobConfig:
    input_path: Path
    output_dir: Path
    max_error_rate: float = 0.1
    log_level: str = "INFO"


def load_config(env: Mapping[str, str]) -> JobConfig:
    problems: list[str] = []
    for name in ("JOB_INPUT", "JOB_OUTPUT_DIR"):
        if not env.get(name):
            problems.append(f"{name} is required")
    rate = 0.1
    raw_rate = env.get("JOB_MAX_ERROR_RATE")
    if raw_rate is not None:
        try:
            rate = float(raw_rate)
            if not 0 <= rate <= 1:
                raise ValueError
        except ValueError:
            problems.append("JOB_MAX_ERROR_RATE must be a number between 0 and 1")
    level = env.get("JOB_LOG_LEVEL", "INFO").strip().upper()
    if level not in LEVELS:
        problems.append(f"JOB_LOG_LEVEL must be one of {sorted(LEVELS)}")
    if problems:
        raise ConfigError("; ".join(problems))
    return JobConfig(Path(env["JOB_INPUT"]), Path(env["JOB_OUTPUT_DIR"]), rate, level)
