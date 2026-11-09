import argparse
import os
import sys

from jobrunner.config import ConfigError, load_config
from jobrunner.logs import setup_logging
from jobrunner.runner import run_job


def main(argv=None, env=None) -> int:
    parser = argparse.ArgumentParser(prog="jobrunner")
    parser.add_argument("--input")
    parser.add_argument("--output-dir")
    parser.add_argument("--max-error-rate")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    merged = dict(os.environ if env is None else env)
    if args.input:
        merged["JOB_INPUT"] = args.input
    if args.output_dir:
        merged["JOB_OUTPUT_DIR"] = args.output_dir
    if args.max_error_rate is not None:
        merged["JOB_MAX_ERROR_RATE"] = args.max_error_rate
    if args.verbose:
        merged["JOB_LOG_LEVEL"] = "DEBUG"

    try:
        config = load_config(merged)
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    logger = setup_logging(config.log_level)
    try:
        stats = run_job(config, logger)
    except FileNotFoundError as exc:
        print(f"error: input not found: {exc.filename}", file=sys.stderr)
        return 3

    print(f"total={stats.total} good={stats.good} rejected={stats.rejected}")
    if stats.total == 0:
        print("error: no input rows", file=sys.stderr)
        return 1
    if stats.error_rate > config.max_error_rate:
        print(
            f"error: error rate {stats.error_rate:.1%} exceeds budget of {config.max_error_rate:.1%}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
