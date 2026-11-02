import argparse
import sys
from pathlib import Path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="rowcount")
    parser.add_argument("path", type=Path)
    parser.add_argument("--skip-header", action="store_true")
    args = parser.parse_args(argv)
    try:
        lines = [ln for ln in args.path.read_text().splitlines() if ln.strip()]
    except OSError as exc:
        print(f"error: cannot read {args.path}: {exc.strerror}", file=sys.stderr)
        return 1
    if args.skip_header:
        lines = lines[1:]
    print(len(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
