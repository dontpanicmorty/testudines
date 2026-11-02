"""Command line entry point."""
import argparse
import logging

from .run import run_pipeline

log = logging.getLogger("pipeline")


def main(argv: list[str] | None = None) -> int:
    """Parse argv, run the pipeline, return an exit code (0 ok, 2 missing input file)."""
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
