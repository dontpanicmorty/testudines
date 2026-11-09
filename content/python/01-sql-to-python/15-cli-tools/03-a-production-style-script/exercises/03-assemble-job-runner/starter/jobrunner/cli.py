import os
import sys

from jobrunner.config import ConfigError, load_config
from jobrunner.logs import setup_logging
from jobrunner.runner import run_job


def main(argv=None, env=None) -> int:
    # TODO: argparse (--input, --output-dir, --max-error-rate, -v), config, logging, run, exit code
    raise NotImplementedError


if __name__ == "__main__":
    sys.exit(main())
