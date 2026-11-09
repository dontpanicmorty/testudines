from pathlib import Path

import pytest

from jobrunner.config import ConfigError, load_config

BASE = {"JOB_INPUT": "in.csv", "JOB_OUTPUT_DIR": "out"}


def test_defaults_and_paths():
    c = load_config(BASE)
    assert c.input_path == Path("in.csv") and c.output_dir == Path("out")
    assert c.max_error_rate == 0.1 and c.log_level == "INFO"


def test_overrides():
    c = load_config({**BASE, "JOB_MAX_ERROR_RATE": "0.25", "JOB_LOG_LEVEL": "debug"})
    assert c.max_error_rate == 0.25 and c.log_level == "DEBUG"


def test_all_problems_named():
    with pytest.raises(ConfigError) as info:
        load_config({"JOB_MAX_ERROR_RATE": "2", "JOB_LOG_LEVEL": "loud"})
    msg = str(info.value)
    for name in ("JOB_INPUT", "JOB_OUTPUT_DIR", "JOB_MAX_ERROR_RATE", "JOB_LOG_LEVEL"):
        assert name in msg, f"{name} not in {msg!r}"


@pytest.mark.parametrize("bad", ["abc", "-0.1", "1.01"])
def test_bad_rate(bad):
    with pytest.raises(ConfigError, match="JOB_MAX_ERROR_RATE"):
        load_config({**BASE, "JOB_MAX_ERROR_RATE": bad})
