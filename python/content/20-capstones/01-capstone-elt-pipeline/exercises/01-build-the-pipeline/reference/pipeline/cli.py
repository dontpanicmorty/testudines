"""Command line entry point."""
import argparse
import logging

from .run import run_pipeline

log = logging.getLogger("pipeline")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pipeline", description="Load daily revenue from order CSVs.")
    p.add_argument("--data-dir", required=True)
    p.add_argument("--db", required=True)
    p.add_argument("--incremental", action="store_true")
    p.add_argument("-v", "--verbose", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    try:
        run_pipeline(args.data_dir, args.db, incremental=args.incremental)
    except FileNotFoundError as exc:
        log.error("input file missing: %s", exc.filename)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
